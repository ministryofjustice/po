from base64 import b64decode

from django.conf import settings
from django.utils import timezone

from po.lib.gemfile import Gemfile
from models import Repository
from pygithub import Github, GithubException


def set_timezone(dt):
    """Github returns datetimes in the client's local timezone"""
    return dt.replace(tzinfo=timezone.get_current_timezone())


def record_gem_dependencies(gh_repo, repo_model):
    try:
        gemfile = gh_repo.get_file_contents('Gemfile.lock')
        gemfile = Gemfile(b64decode(gemfile.content))
        for name, version in gemfile.dependencies:
            print ' -', name, version
            repo_model.add_dependency(name, version, 'RubyGems')
    except GithubException:
        # no Gemfile.lock
        pass


def find_rspec_tests(gh_repo):
    try:
        spec_dir = gh_repo.get_contents('spec')
        return isinstance(spec_dir, list) and len(spec_dir) > 0

    except GithubException:
        return False


def find_ruby_tests(gh_repo):
    if find_rspec_tests(gh_repo):
        return True
    return False


def find_python_unittests(gh_repo):
    gh = Github(settings.GITHUB_TOKEN)
    try:
        results = gh.search_code(
            'TestCase language:python repo:{repo}'.format(
                repo=gh_repo.full_name))
        return len(list(results)) > 0

    except GithubException:
        return False


def find_python_tests(gh_repo):
    if find_python_unittests(gh_repo):
        return True
    return False


TEST_FINDERS = {
    'ruby': find_ruby_tests,
    'python': find_python_tests,
}


def null_finder(gh_repo):
    return False


def tests_exist(lang, gh_repo):
    test_finder = TEST_FINDERS.get(lang.lower(), null_finder)
    return test_finder(gh_repo)


def check_for_tests(gh_repo, repo_model):
    for lang in repo_model.languages_by_usage():
        if tests_exist(lang, gh_repo):
            return True
    return False


def spider_repos():
    gh = Github(settings.GITHUB_TOKEN)
    for repo in gh.get_organization('ministryofjustice').get_repos():
        r = Repository()
        r.name = repo.name
        r.created = set_timezone(repo.created_at)
        r.updated = set_timezone(repo.updated_at)
        r.description = repo.description
        r.private = repo.private
        r.url = repo.html_url
        r.contributors = repo.get_contributors().totalCount or 0
        r.save()
        print '\nSaving', r.name

        r.add_language_usages(repo.get_languages())

        record_gem_dependencies(repo, r)

        check_for_tests(repo, r)

        r.save()

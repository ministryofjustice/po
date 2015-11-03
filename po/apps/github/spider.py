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

        r.save()

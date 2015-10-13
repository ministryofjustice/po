from base64 import b64decode

from django.conf import settings
from django.utils import timezone
from github import Github, GithubException

from po.lib.gemfile import Gemfile
from models import Repository, Dependency, Package, LanguageUsage


def set_timezone(dt):
    """Github returns datetimes in the client's local timezone"""
    return dt.replace(tzinfo=timezone.get_current_timezone())


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
        for language, num_bytes in repo.get_languages().iteritems():
            usage = LanguageUsage()
            usage.language = language
            usage.num_bytes = num_bytes
            r.languages.add(usage)

        try:
            gemfile = repo.get_file_contents('Gemfile.lock')
            gemfile = Gemfile(b64decode(gemfile.content))
            for name, version in gemfile.dependencies:
                print ' -', name, version
                # XXX get a version object because string comparison is buggy
                ver = Package(version=version).version
                package, created = Package.objects.get_or_create(
                    name=name, version=ver, source='RubyGems')
                if created:
                    package.save()
                dep = Dependency()
                dep.package = package
                dep.dependant = r
                dep.save()
        except GithubException:
            # no Gemfile.lock
            pass

        r.save()

from django.conf import settings
from django.utils import timezone
from github import Github
import pytz

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
            print ' -', language, '({0})'.format(num_bytes)
            r.languages.add(usage)
        r.save()

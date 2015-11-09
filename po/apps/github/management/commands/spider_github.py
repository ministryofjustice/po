from django.core.management.base import BaseCommand, CommandError
from github.spider import spider_repos


class Command(BaseCommand):
    help = 'Gathers repository metadata from Github'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        spider_repos()

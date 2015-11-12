from django.core.management.base import BaseCommand, CommandError
from incident_response.zendesk_client import check_incidents


class Command(BaseCommand):
    help = 'Count incidents per service on Zendesk'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        check_incidents()

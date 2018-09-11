import logging

from apps.context.tasks import load_activities
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''
    Запуск синхронизации активностей
    '''

    def handle(self, *args, **options):
        logging.info("Activity sync called")
        load_activities.apply_async()

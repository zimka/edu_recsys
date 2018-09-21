import logging

from django.core.management.base import BaseCommand

from apps.activity.tasks import update_activity_recommendations


class Command(BaseCommand):
    help = '''
    Запуск обновления рекомендаций активности
    '''

    def handle(self, *args, **options):
        logging.info("Activity Recommendations run_update_async called")
        update_activity_recommendations()

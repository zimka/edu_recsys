import logging
from django.core.management.base import BaseCommand
from apps.activity.manager import ActivityRecommendationManager


class Command(BaseCommand):
    help = '''
    Запуск обновления рекомендаций активности
    '''

    def handle(self, *args, **options):
        logging.info("Activity Recommendations run_update_async called")
        ActivityRecommendationManager().run_update_async()

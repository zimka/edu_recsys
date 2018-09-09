from django.core.management.base import BaseCommand
from apps.networking.tasks import create_networking_recommendations
from apps.context.models import Student


class Command(BaseCommand):
    help = '''
    Запуск обновления рекомендаций активности
    '''

    def handle(self, *args, **options):
        users = Student.objects.filter(networkingrecommendation=None)
        for u in users:
            create_networking_recommendations.delay(u.uid)

from django.core.management.base import BaseCommand
from apps.networking.tasks import create_networking_recommendations


class Command(BaseCommand):
    help = '''
    Запуск обновления рекомендаций контактов
    '''
    def add_arguments(self, parser):
        parser.add_argument('--overwrite', dest='overwrite', type=str, default=False, help=u'Перезаписать текущие рекомендации')


    def handle(self, *args, **options):
        overwrite = options.get('overwrite', False)
        create_networking_recommendations.delay(overwrite)

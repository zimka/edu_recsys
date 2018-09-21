from django.core.management.base import BaseCommand

from apps.networking.tasks import update_networking_recommendations


class Command(BaseCommand):
    help = '''
    Запуск обновления рекомендаций контактов
    '''
    def add_arguments(self, parser):
        parser.add_argument('--for_new_only', dest='for_new_only', type=str, default=False, help=u'Только для юзеров без рекоммендаций')

    def handle(self, *args, **options):
        for_new_only = options.get('for_new_only', True)
        update_networking_recommendations(for_new_only=for_new_only)

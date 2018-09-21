from django.core.management.base import BaseCommand

from apps.interpreter.models import SingleScoreComputeTask


class Command(BaseCommand):
    help = '''
    Запуск вычислений неоконченных задач
    '''

    def handle(self, *args, **options):
        tasks = SingleScoreComputeTask.objects.filter(complete=False)
        for t in tasks:
            t.compute_async()

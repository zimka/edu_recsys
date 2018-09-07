import logging
from celery import shared_task


log = logging.getLogger(__name__)


@shared_task
def compute_single_score_async(uuid):
    from .models import SingleScoreComputeTask
    try:
        ctask = SingleScoreComputeTask.objects.get(uuid=uuid)
    except SingleScoreComputeTask.DoesNotExist:
        log.error("Compute task execution: wrong uuid :'{}'".format(uuid))
        return False
    ctask.compute()

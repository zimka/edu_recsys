import logging

from celery import shared_task, chain

from apps.networking.tasks import update_networking_recommendations

log = logging.getLogger(__name__)


def run_update(uuid):
    pass
    #chain(compute_single_score_async.s(uuid), update_networking_recommendations().si())()

@shared_task
def compute_single_score_async(uuid):
    from .models import SingleScoreComputeTask
    try:
        ctask = SingleScoreComputeTask.objects.get(uuid=uuid)
    except SingleScoreComputeTask.DoesNotExist:
        log.error("Compute task execution: wrong uuid :'{}'".format(uuid))
        return False
    ctask.compute()

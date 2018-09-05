import logging
from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def update_activity_recommendations(manager, **kwargs):
    return manager.do_update(**kwargs)

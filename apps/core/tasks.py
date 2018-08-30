import logging

from celery.task import task

log = logging.getLogger(__name__)

@task
def update_activity_recommendations(manager, **kwargs):
    return manager.do_update(**kwargs)

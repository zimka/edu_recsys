from datetime import datetime
import logging

from celery import shared_task

log = logging.getLogger(__name__)
from .updater import ActivityRecommendationUpdater


@shared_task

@shared_task
def _update_activity_recommendations(**kwargs):
    start = datetime.now()
    log.info("Started update_activity_recommendations")
    result = ActivityRecommendationUpdater(**kwargs).do_update(**kwargs)
    log.info("Finished update_activity_recommendations, took {}".format(
        datetime.now() - start
    ))
    return result


def update_activity_recommendations(async=True, **kwargs):
    if async:
        return _update_activity_recommendations.apply_async(**kwargs)
    else:
        return _update_activity_recommendations.apply(**kwargs)
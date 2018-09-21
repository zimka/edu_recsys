from datetime import datetime
import logging

from celery import shared_task

log = logging.getLogger(__name__)
from .updater import NetworkingRecommendationUpdater


@shared_task
def _update_networking_recommendations(**kwargs):
    start = datetime.now()
    log.info("Started update_networking_recommendations")
    result = NetworkingRecommendationUpdater(**kwargs).do_update(**kwargs)
    log.info("Finished update_networking_recommendations, took {}".format(
        datetime.now() - start
    ))
    return result


def update_networking_recommendations(async=True, **kwargs):
    if async:
        return _update_networking_recommendations.apply_async(**kwargs)
    else:
        return _update_networking_recommendations.apply(**kwargs)
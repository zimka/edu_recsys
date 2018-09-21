import logging
from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings

from .models import Activity

log = logging.getLogger(__name__)


def _handle_activity_data(data):
    title = data["title"]
    uuid = data["uuid"]

    act, created = Activity.objects.get_or_create(uuid=uuid)
    if act.title != title:
        act.title = title
        act.save()


@shared_task
def load_activities(limit=None):
    start_time = datetime.now()
    log.info("Started Activity loading from LABS :{}".format(str(start_time)))
    base_url = settings.LABS_BASE_URL
    uri = "/api/v1/activity"
    app_token = settings.LABS_APP_TOKEN
    response = requests.get(base_url + uri, params={"app_token": app_token})
    if not response.ok:
        reason = None
        try:
            reason = response.json()
        except:
            pass
        log.error("Failed to fetch activities from LABS, reason: {}".format(reason))
        return False
    try:
        data = response.json()
    except Exception as e:
        log.error("Failed to process data from LABS, reason: {}".format(e))
        return False

    for num, record in enumerate(data):
        try:
            _handle_activity_data(record)
        except Exception as e:
            log.error("Failed to process activity record: {}, error: {}".format(
                str(record['title']),
                str(e)
            ))
        if limit and num>=limit:
            break
    log.info("Successfully finished Activity loading, took {}".format(str(datetime.now() - start_time)))
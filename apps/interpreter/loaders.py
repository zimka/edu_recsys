import logging
import requests
from django.conf import settings


log = logging.getLogger(__name__)


class PleApiClient:
    def __init__(self, base_url=None, app_token=None):
        if base_url is None:
            base_url = settings.PLE_BASE_URL
        if app_token is None:
            app_token = settings.PLE_APP_TOKEN

        self.base_url = base_url
        self.app_token = app_token

        self.uri_dict = {
            "activity_result": "/activity/{uuid}/result"
        }
        self.ple_guid_uuids = settings.PLE_GUID_UUIDS

    def _get_user_result(self, user_uid, activity_uuid):
        uuid = activity_uuid
        uri = self.uri_dict["activity_result"]
        current_url = self.base_url + uri.format(uuid)
        query_params = {
            "app_token": self.app_token,
            "unti_id": user_uid,
        }
        response = requests.get(current_url, query_params=query_params)

        if response.ok:
            return response.json()["results"]
        else:
            try:
                reason = response.json()
            except ValueError:
                reason = None
            log.error("Failed to fetch data from {url} with {query}: {code}, reason - {reason}".format(
                url=current_url, query=query_params, code=response.status_code, reason=reason
            ))

    def get_user_diagnostics(self, user_uid):
        result = {}
        for guid, uuid in self.ple_guid_uuids.items():
            data = self._get_user_result(user_uid, uuid)
            if data:
                result[guid] = data
        return result


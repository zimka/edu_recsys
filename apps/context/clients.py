import json
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
            "activity_result": "/api/v1/activity/{uuid}/result"
        }
        self.ple_guid_uuids = settings.PLE_GUID_UUIDS

    def _get_user_result(self, user_uid, activity_uuid):
        uuid = activity_uuid
        uri = self.uri_dict["activity_result"]
        current_url = self.base_url + uri.format(uuid=uuid)
        query_params = {
            "app_token": self.app_token,
            "unti_id": user_uid,
        }
        response = requests.get(current_url, params=query_params)
        log.info("Fetch data from PLE: {}, {} - {}".format(current_url, query_params, response))
        if response.ok:
            return response.json()["result"]
        else:
            try:
                reason = response.json()
            except ValueError:
                reason = None
            log.error("Failed to fetch PLE data from {url} with {query}: {code}, reason - {reason}".format(
                url=current_url, query=query_params, code=response.status_code, reason=reason
            ))

    def get_user_diagnostics(self, user_uid):
        result = {}
        for guid, uuid in self.ple_guid_uuids.items():
            data = self._get_user_result(user_uid, uuid)
            if data:
                result[guid] = data
        return result


class LrsApiClient:
    def __init__(self, base_url=None, app_token=None, ple_base_url=None):
        if base_url is None:
            base_url = settings.LRS_BASE_URL
        if app_token is None:
            app_token = settings.LRS_AUTH_TOKEN

        if ple_base_url is None:
            ple_base_url = settings.PLE_BASE_URL
        self.base_url = base_url
        self.app_token = app_token
        self.uri_data = "/data/xAPI/statements"
        self.ple_base_url = ple_base_url
        self.archetypes_guid = settings.LRS_ARCHETYPES_GUID

    def _get_user_result(self, unti_id_filter=None, activity_guid_filter=None, get_all=False):
        headers = {
            "Authorization": self.app_token,
            'X-Experience-API-Version': '1.0.3'
        }
        params = {}
        if unti_id_filter is not None:
            params["agent"] = json.dumps(
                    {"account": {'homePage': self.ple_base_url + "/", 'name':str(unti_id_filter)}}
            )

        if activity_guid_filter is not None:
            params["activity"] = self.ple_base_url + "/xapi/v1/activity/"+ activity_guid_filter

        current_url = self.base_url + self.uri_data
        response = requests.get(self.base_url + self.uri_data, params=params, headers=headers)
        log.info("Fetch data from LRS: {}, {} - {}".format(current_url, params, response))

        if response.ok:
            statements = response.json()["statements"]
            if not len(statements):
                return
            if get_all:
                return statements
            last_statement = statements[0]
            return last_statement['result']
        else:
            try:
                reason = response.json()
            except ValueError:
                reason = None
            log.error("Failed to fetch LRS data from {url} with {query}: {code}, reason - {reason}".format(
                url=current_url, query=params, code=response.status_code, reason=reason
            ))

    def get_archetypes(self, unti_id):
        return self._get_key(unti_id, "archetypes")

    def get_motivalis(self, unti_id):
        return self._get_key(unti_id, "motivation")

    def _get_key(self, unti_id, key):
        data = self._get_user_result(str(unti_id), self.archetypes_guid)
        if data is not None:
            try:
                ext = data['extensions']
                k = self.ple_base_url + "/xapi/v1/results/{}".format(key)
                return ext[k]
            except KeyError as e:
                log.error("LRS fetch error:{}".format(e))
                return None


class DpApiClient:

    def __init__(self, base_url=None, app_token=None):
        if base_url is None:
            base_url = settings.DP_BASE_URL
        if app_token is None:
            app_token = settings.DP_APP_TOKEN

        self.base_url = base_url
        self.app_token = app_token

        self.single_score_uri = "/api/v1/user/{unti_id}"

    def set_single_score(self, unti_id, single_score_dict):
        url = self.base_url + self.single_score_uri.format(unti_id=unti_id)
        payload = single_score_dict
        params = {"app_token": self.app_token}
        response = requests.post(url, params=params, json=payload)
        if not response.ok:
            reason = None
            try:
                reason = response.json()
            except:
                pass
            log.error("Failed to push single_score to dp: {}, {}, {} - {}".format(url, params,payload,reason))
            return False
        return True

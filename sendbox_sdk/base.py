import datetime as dt
from typing import Dict, Union, List
from urllib import parse as urllib_parse

import requests

from .const import SENDBOX_API_ENDPOINT, METHOD_PATHS


class ApiBase:
    def get_url(self, path):
        return urllib_parse.urljoin(SENDBOX_API_ENDPOINT, path)

    def __init__(self, ID: str, secret: str):
        self.id = ID
        self.secret = secret
        self._auth_token = None
        self._token_expire_time = None

    def _token_renew_required(self):
        """
        Check conditions for token renewal
        :return:
        """
        current_time = dt.datetime.now()
        return not self._token_expire_time or current_time > self._token_expire_time

    def _obtain_auth_token(self):
        current_time = dt.datetime.now()
        params = {
            'grant_type': "client_credentials",
            'client_id': self.id,
            'client_secret': self.secret,
        }
        result = self._post_request(METHOD_PATHS.auth, params, token_required=False)
        self._auth_token = result['access_token']
        self._token_expire_time = current_time + dt.timedelta(minutes=result['expires_in'])


    def _make_request(self, request_type: str,
                      url: str,
                      data: Dict[str, Union[str, float, int]] = None,
                      json: Dict[str, Union[str, float, int]] = None,
                      token_required: bool = True):
        """
        Sending request to Sendbox
        :return:
        """
        if token_required and self._token_renew_required():
            self._obtain_auth_token()

        assert request_type in ('post', 'get'), "'request_type' should be one of: 'post', 'get'"
        full_path = self.get_url(url)
        r = requests.request(request_type, full_path, data=data, json=json,
                             headers={"Authorization": "Bearer %s" % self._auth_token})
        assert r.status_code == 200, "Wrong status code"
        return r.json()

    def _post_request(self, url: str,
                      data: Union[Dict[str, Union[Dict, List, str, float, int]], List[Dict]],
                      **kwargs):
        """
        POST request to sendbox api
        """
        return self._make_request('post', url, json=data, **kwargs)

    def _get_request(self, url, params=None, **kwargs):
        return self._make_request('get', url, data=params, **kwargs)

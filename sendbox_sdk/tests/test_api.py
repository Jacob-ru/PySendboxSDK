
from mock import patch, Mock

from sendbox_sdk.api import SendBoxApi


class TestSendBoxApi:
    ID = '<id>'
    secret = '<secret>'

    def get_api(self):
        return SendBoxApi(self.ID, self.secret)

    def test_obtain_token(self):
        api = self.get_api()

        result = {
            "access_token": "<access_token>",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        request_mock = Mock(
            status_code=200,
            json=Mock(return_value=result)
        )
        with patch('requests.request', return_value=request_mock):
            api._obtain_auth_token()
            assert api._token_expire_time
            assert api._auth_token == "<access_token>"

    def test_obtain_token_on_make_request(self):
        api = self.get_api()
        request_mock = Mock(
            status_code=200,
            json=Mock(return_value={})
        )
        obtain_token_mock = Mock()
        with patch.object(api, '_obtain_auth_token', obtain_token_mock), \
             patch('requests.request', return_value=request_mock):
            api._make_request("post", "test_url", {})
            assert obtain_token_mock.call_count == 1

    def test_getting_total_emails(self):
        api = self.get_api()
        api._auth_token = 'token'
        request_mock = Mock(
            status_code=200,
            json=Mock(return_value={'total': 10})
        )
        with patch('requests.request', return_value=request_mock), \
             patch.object(api, '_token_renew_required', return_value=False):
            res = api.emails_total()
            assert res['total'] == 10
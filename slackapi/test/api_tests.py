__author__ = 'NiCoretti'

import json
import unittest
import urllib
import http.client
import slackapi

from unittest.mock import MagicMock
from slackapi.api import SlackApiRequest, SlackApiResponse, SlackApi

class ApiRequestTests(unittest.TestCase):

    def setUp(self):
        self.api_call = 'api.test'
        self.token = "TestToken"
        self.http_status_code = http.client.OK
        self.mocked_https_connection = MagicMock()
        self.mocked_https_response = MagicMock()
        self.parameters = {"token": self.token}

    def tearDown(self):
        self.mocked_https_connection.reset_mock()

    def test_api_request_is_successful(self):
        api_call = "api.test"
        parameters = urllib.parse.urlencode(self.parameters)
        api_request = SlackApiRequest(api_call, self.token)
        response_data = {'ok': True, 'args': {'foo': 'bar'}}
        response_json = json.dumps(response_data)
        response_data = bytes(response_json.encode("utf-8"))
        self.mocked_https_response.status = http.client.OK
        self.mocked_https_response.read = MagicMock(return_value=response_data)
        self.mocked_https_connection.getresponse = MagicMock(return_value=self.mocked_https_response)
        api_request._connection = self.mocked_https_connection

        api_request.execute("api.test")
        expected_call_url = slackapi.api.API_BASE_URL + api_call + "?" + parameters
        self.mocked_https_connection.request.assert_called_with("GET", expected_call_url)

    def test_api_request_is_fails_because_of_invalid_http_status(self):
        api_call = "api.test"
        parameters = urllib.parse.urlencode(self.parameters)
        api_request = SlackApiRequest(api_call, self.token)
        response_data = {'ok': True, 'args': {'foo': 'bar'}}
        response_json = json.dumps(response_data)
        response_data = bytes(response_json.encode("utf-8"))
        self.mocked_https_response.status = http.client.BAD_REQUEST
        self.mocked_https_response.read = MagicMock(return_value=response_data)
        self.mocked_https_connection.getresponse = MagicMock(return_value=self.mocked_https_response)
        api_request._connection = self.mocked_https_connection

        self.assertRaises(Exception, api_request.execute, "api.test")


class ApiResponseTests(unittest.TestCase):

    def test_json_parse_error_in_init(self):
        malformed_input_data = "some text which is no json"
        self.assertRaises(ValueError, SlackApiResponse, malformed_input_data)

    def test_is_error_indicates_api_call_failure(self):
        input_data = {"ok": False, "error": "more detailed error message"}
        input_data = json.dumps(input_data)
        response = SlackApiResponse(input_data)
        self.assertTrue(response.is_error())

    def test_is_error_indicates_that_api_call_was_successful(self):
        input_data = {"ok": True }
        input_data = json.dumps(input_data)
        response = SlackApiResponse(input_data)
        self.assertFalse(response.is_error())


class ApiTests(unittest.TestCase):

    def test_unknown_api_call_is_called(self):
        authentication_token = "The token isn't relevant for this test"
        slackapi = SlackApi(authentication_token)
        unknown_api_call = "this.api.method.does.not.exist"
        self.assertRaises(Exception, slackapi.call, unknown_api_call)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
#
# Copyright (c) 2014, Nicola Coretti
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
__version__ = "0.0.1"
__author__ = 'Nicola Coretti'
__email_ = 'nico.coretti@gmail.com'

import sys
import json
import argparse
import urllib.parse
import http.client

API_BASE_URL = "https://slack.com/api/"
SLACK_DOMAIN = "www.slack.com"

class SlackApi(object):
    """
    A SlackApi object can be used to interact with the slack api.
    :see https://api.slack.com/methods
    """
    SLACK_API_CALLS = {'api.test', 'auth.test', 'channels.archive',
                       'channels.create', 'channels.history', 'channels.info',
                       'channels.invite', 'channels.join', 'channels.kick',
                       'channels.leave', 'channels.list', 'channels.mark',
                       'channels.rename', 'channels.setPurpose', 'channels.setTopic',
                       'channels.unarchive', 'chat.delete', 'chat.postMessage',
                       'chat.update', 'emoji.list', 'files.info', 'files.list',
                       'files.upload', 'groups.archive', 'groups.close',
                       'groups.create', 'groups.createChild', 'groups.history',
                       'groups.invite', 'groups.kick', 'groups.leave', 'groups.list',
                       'groups.mark', 'groups.open', 'groups.rename', 'groups.setPurpose',
                       'groups.setTopic', 'groups.unarchive', 'im.close', 'im.history',
                       'im.list', 'im.mark', 'im.open', 'oauth.access', 'presence.set',
                       'rtm.start', 'search.all', 'search.files', 'search.messages',
                       'stars.list', 'users.info', 'users.list', 'users.setActive'}

    def __init__(self, authentication_token):
        """
        Creates a new Slack-Api object which can be used to interact with the slack api.

        :param token: which grants autheticated access to the slack api.
        """
        self._authentication_token = authentication_token

    def call(self, api_call, parameters=None):
        """
        Executes a call on the remote slack api and returns
        an appropriate ApiResponse object.

        :return an ApiResponse object containing the data provided
                by the slackapi endpoint.

        :raise Exception if an unknown api method is called.
        """
        if api_call not in SlackApi.SLACK_API_CALLS:
            error_message = "Unknown api method was called"
            raise Exception(error_message)
        else:
            request = SlackApiRequest(api_call, self._authentication_token)
            response = request.execute(parameters)
            return response


class SlackApiRequest(object):

    def __init__(self, api_call, authentication_token):
        """
        Creates a new ApiRequest object for the specified api call.

        :param api_call name of the api method which shall be callable by the request object.
        :param authentication_token which will be used to authorize the api call request.
        """
        self._api_call = api_call
        self._authentication_token = authentication_token
        self._connection = http.client.HTTPSConnection(SLACK_DOMAIN)

    def execute(self, request_parameters=None):
        """
        Executes an ApiRequest, request an api call.

        :param request_parameters: a dictionary containing the parameters for the api call.
        :param authentication_token: which grants access to the api.

        :return an ApiResponse object based on the response of the slackapi endpoint.

        :raise Exception if an error occurs while executing the api call.
        """
        parameters = {}
        parameters.update({'token': self._authentication_token})
        if isinstance(request_parameters, dict):
            parameters.update(request_parameters)

        parameters = urllib.parse.urlencode(parameters)
        api_call_endpoint = API_BASE_URL + self._api_call
        self._connection.request("GET", api_call_endpoint + "?" + parameters)
        response = self._connection.getresponse()

        if response.status is not http.client.OK:
            error_message = "Error while executing api call, details {0}"
            error_message = error_message.format(response)
            raise Exception(error_message)
        else:
            response_data = response.read()
            return SlackApiResponse(response_data.decode('utf-8'))


class SlackApiResponse(object):
    """
    The ApiResponse class handles and encapsulates an response provided
    by the slackapi after an api method was called at the endpoint.
    """

    def __init__(self, response_data):
        """
        Interprets a response of slack api call and creates the appropriate ApiResponse object.

        :param response_data: a json string which is a valid response for
                              a slackapi call :see https://api.slack.com/methods.
        """
        self.data = json.loads(response_data)

    def is_error(self):
        """
        Indicates whether or not the response indicates that an
        error occured while trying to execute the associated api call.

        :return True if an error has occurred, otherwise False.
        """
        if 'ok' in self.data:
            return not self.data['ok']
        else:
            return True

    def get_error_message(self):
        """
        If is_error returns True, this method returns a more detail
        error message.

        :return a string which provides a more detail error message.
        """
        if 'error' in self.data:
            return self.data['error']
        else:
            return 'No Error'


def main():
    cmd_args_parser = create_argparser_for_slackapi_cmd()
    arguments = cmd_args_parser.parse_args()

    api = SlackApi(arguments.authentication_token)
    api_method = arguments.api_method
    parameters = ""
    if arguments.parameters:
        try:
            parameters = parse_parameters(arguments.parameters)
        except:
            print("Invalid parameter string", file=sys.stderr)
            sys.exit(-1)
    response = api.call(api_method, parameters)
    print(response.data)

def create_argparser_for_slackapi_cmd():
    parser = argparse.ArgumentParser(description='Slack Api command line tool')
    parser.add_argument('api_method',  default='api.test',
                        help='Api method which shall be called')
    parser.add_argument('-p', '--params', metavar='Parameters', dest='parameters',
                        help='Parameters which shall be passed to the api call'
                        + '. The should be a string in the format: "parameter: value, parameter: value"')
    parser.add_argument('-t', '--token', metavar='ApiToken', dest='authentication_token',
                        default= 'xoxb-3171438313-1v5ei3JGK3nabyTiMDCHK5Ek',
                        help='token used to provide authenticate against the slack api')
    return parser

def parse_parameters(parameter_string):
    parameters = dict((key.strip(), value.strip()) for key, value in (pair.split(':') for pair in parameter_string.split(',')))
    return parameters

if __name__ == "__main__":
    main()


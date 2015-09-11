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

import json
import logging
import collections
import slackapi.api
import websocket.client

# Set up logging
LOGGER = logging.getLogger()
formatter = logging.Formatter('%(levelname)s: - %(module)s - %(funcName)s - Message: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)
LOGGER.setLevel(logging.DEBUG)


# TODO: add logger output!
class SlackBot(object):
    """
    This bot just encapsultes the gerneral bot tasks
    """

    def __init__(self, authentication_token):
        """
        Creates a new slack bot.

        :param authentication_token: which will be used to interact with the slack api.
        """
        self._websocket_client = None
        self._authentication_token = authentication_token
        self._slack_api = slackapi.api.SlackApi(self._authentication_token)
        # in order to keep the connection alive slack rtm needs to now that we are still alive
        # therefore it wants to get a ping every once in a while, we need this timeout to
        # keep track when we have to ping again.
        self._ping_timeout = 10
        # TODO: add reate limit control
        # self._rate_limit in ms


    def connect(self):
        LOGGER.info('Connecting to slack server')
        rtm_start_response = self._slack_api.call("rtm.start")
        rtm_websocket_url = rtm_start_response.data["url"]
        self._websocket_client = websocket.client.WsClient(rtm_websocket_url)
        self._websocket_client.connect()
        self._websocket_client.register_message_received_callback(self._received_message)
        LOGGER.debug('Connection to slack server established')


    def run_forever(self):
        self._websocket_client.run_forever()


    def disconnect(self):
        LOGGER.info('Closed connection')


    def _received_message(self, message):
        # might add the utf-8 decoding here so subclasses dont have to deal
        # with this issue
        LOGGER.debug('Received message: {0}'.format(message))


    def _connection_lost(self):
        LOGGER.debug('Connection lost')
        self.connect()


class EchoBot(SlackBot):
    """
    EchoBot echos all text message send to any channel he has joined.
    """

    def __init__(self, authentication_token):
        super(EchoBot, self).__init__(authentication_token)


    def _received_message(self, message):
        message = json.loads(message.decode("utf-8"))
        if ('type' in message) and (message['type'] == 'message'):
            response_ditc = {}
            response_ditc['id'] = 1
            if 'text' in message:
                response_ditc['text'] = message['text']
            else:
                response_ditc['text'] = "-- could not echo the original message --"
            response_ditc['type'] = 'message'
            if 'channel' in message:
                response_ditc['channel'] = message['channel']
            json_response = json.dumps(response_ditc)
            self._websocket_client.send(json_response)
        else:
            pass


class SirTalkALot(SlackBot):
    """
    Provides extensible module based services.
    """

    def __init__(self, api_token, modules):
        super(SirTalkALot, self).__init__(api_token)
        self._modules = collections.defaultdict()
        for module in modules:
            pass

    def _parse_raw_message(self, message):
        pass

    def _received_message(self, message):
        message = json.loads(message.decode("utf-8"))
        if ('type' in message) and not (message['type'] == 'message'):
            pass
        else:
            pass

    def register_module(self, module):
        self._modules.append(module)

    def unregister_module(self, module):
        pass


if __name__ == "__main__":
    api_token = 'Your API-Token goes here'
    api_token = 'xoxb-3171438313-fK52hNR3cz55KZjAMDWNIgI9'
    bot = EchoBot(api_token)
    bot.connect()
    bot.run_forever()

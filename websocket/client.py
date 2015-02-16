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

import logging
import ws4py.client.threadedclient

LOGGER = logging.getLogger(__name__)

class WsClient(ws4py.client.threadedclient.WebSocketClient):

    def opened(self):
        LOGGER.debug('websocket connection opened')

    def closed(self, code, reason):
        LOGGER.debug('websocket connection closed')

    def register_message_received_callback(self, callback):
        self._message_recieved_callback = callback
        LOGGER.debug('registered message received callback. Callback: {0}'.format(callback))

    def received_message(self, message):
        LOGGER.debug('Received message, message: {0}'.format(message))
        self._message_recieved_callback(message.data)


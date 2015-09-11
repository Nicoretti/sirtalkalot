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
import argparse

from bot import sirtalkalot

# Set up logging
LOGGER = logging.getLogger()
formatter = logging.Formatter('%(levelname)s: - %(module)s - %(funcName)s - Message: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)
LOGGER.setLevel(logging.DEBUG)
#TODO: Depending on the OS (Linux/Win) add syslog or nt loggger

class SirTalkAlotDeamon(object):

    def __init__(self):
        self._logging_nologging = 'NOLOGGING'
        self._logging_debug = 'DEBUG'
        self._logging_info = 'INFO'
        self._logging_warning = 'WARNING'
        self._logging_error = 'ERROR'
        self._logging_critical = 'CRITICAL'
        self._logging_choices = [self._logging_nologging, self._logging_debug,
                                 self._logging_info, self._logging_warning,
                                 self._logging_error, self._logging_critical]
        self._echo_bot_option = 'EchoBot'
        self._sirtalkalot_bot_option = 'SirTalkAlot'
        self._bot_choices = [self._echo_bot_option, self._sirtalkalot_bot_option]


    def _create_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config',
                            help='path to the configuration file which shall bes used.')
        parser.add_argument('--auth-token',
                            help='Authentication token which will be sued to authenticate against the slack api')
        parser.add_argument('--bot', default=self._echo_bot_option, choices=self._bot_choices,
                            help='Selects the type of bot which will be used.')
        parser.add_argument('--loglevel', default=self._logging_info, choices=self._logging_choices,
                            help='Sets the log level used for the SirTalkAlotDeamon.')

        return parser


    def run(self):
        pass


    def main(self, args):
        slack_bot = sirtalkalot.EchoBot()
        slack_bot.run_forever()


if __name__ == '__main__':
    deamon = SirTalkAlotDeamon()
    deamon.run()

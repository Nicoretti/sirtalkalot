# SirTalkAlot

SirTalkAlot is a Slack (RTM) based bot.
The SirTalkAlot package can also be used to create another
Slack (RTM) based bot.

The project is split into 3 different packages.

1. bot
2. slackapi
3. websocket

## bot
This is the only package which is relevant for people which just wanna
create their slack or wanna extend the SirTalkAlot bot.

## slackapi
This module provides a small wrapper for the web based slack api.

## websocket
This module contains a websocket client which is necessary to use
the RTM. SirTalkAlot currently does not provide it's own implementation, he
just uses a small wrapper around the ws4py web socket client.
See [ws4py](https://ws4py.readthedocs.org/en/latest/)

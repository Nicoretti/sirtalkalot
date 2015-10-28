SirTalkAlot
===========

SirTalkAlot is a Slack (RTM) based bot which provides a simple service based slack bot.

Project Structure
+++++++++++++++++++++++++++++++++++++++++++++++
The project is split into 3 different modules.

* bot
* services
* websocket

bot
++++
TBD

services
++++++++
TBD

websocket
+++++++++
This module contains a websocket client which is necessary to use
the RTM. SirTalkAlot currently does not provide it's own implementation, he
just uses a small wrapper around the ws4py web socket client.
See `ws4py <https://ws4py.readthedocs.org/en/latest/>`_.

SirTalkAlot
===========

.. image:: https://travis-ci.org/Nicoretti/sirtalkalot.svg?branch=master
    :target: https://travis-ci.org/Nicoretti/sirtalkalot

.. image:: https://coveralls.io/repos/Nicoretti/sirtalkalot/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/Nicoretti/sirtalkalot?branch=master

.. image:: https://readthedocs.org/projects/sirtalkalot/badge/?version=latest
    :target: http://sirtalkalot.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.waffle.io/Nicoretti/sirtalkalot.png?label=ready&title=Ready
    :target: https://waffle.io/Nicoretti/sirtalkalot
    :alt: 'Stories in Ready'


SirTalkAlot is a Slack (RTM) based bot which provides a simple service based slack bot.

Project Structure
+++++++++++++++++
The project is split into 3 different modules.

* bot
* services
* websocket

bot
+++
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

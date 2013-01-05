# -*- coding: utf-8 -*-

"""
Digital Ocean's API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> from dop.client import Client
   >>> c = Client('client_id', 'api_key')
   >>> regions = client.regions()
   >>> for region in regions:
   >>>     print region.to_json()
   {'id': 1, 'name': u'New York 1'}
   {'id': 2, 'name': u'Amsterdam 1'}

:license: MIT, see LICENSE for more details.

"""

__title__ = 'dop'
__version__ = '0.1.2'
__build__ = 0x000102
__author__ = 'Antonio Hinojo'
__license__ = 'MIT'

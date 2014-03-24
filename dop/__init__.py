# -*- coding: utf-8 -*-

"""
Digital Ocean's API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic usage:

   >>> from dop.client import Client
   >>> c = Client('client_id', 'api_key')
   >>> regions = client.regions()
   >>> for region in regions:
   >>>     print region.to_json()
   {'id': 1, 'name': u'New York 1'}
   {'id': 2, 'name': u'Amsterdam 1'}

:license: MIT, see LICENSE for more details.

"""

from pkg_resources import get_distribution

__title__ = 'dop'
__version__ = get_distribution('dop').version
__author__ = 'Antonio H Montero'
__license__ = 'MIT'

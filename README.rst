DOP: Digital Ocean API Python Wrapper
=====================================

DOP is a MIT licensed Python wrapper for Digital Ocean's API.


Features
--------

Full support for all methods listed `here`_

Installation
------------

To install dop, simply: ::

    $ pip install dop


Example
-------
It is pretty easy to use:

.. code-block:: python

    from dop.client import Client

    client = Client('client_id', 'api_key')
    
    # Print regions.
    regions = client.regions()
    for region in regions:
        print(region.to_json())


Contribute
----------
Pull requests and improvements are welcome.

.. _`here`: https://www.digitalocean.com/api

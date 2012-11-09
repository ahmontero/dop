DOP: Digital Ocean API Python Wrapper
=====================================

DOP is a MIT licensed Python wrapper for Digital Ocean's API.


Features
--------

Full support for all methods listed `here`_ except (they have weird behaviour):
    reset_root_password
    restore
    destroy_image

Experimental support for ssh. Digital Ocean does not have full support for ssh creation, edit and deletion of ssh keys. This wrapper will be updated when they change it.


Installation
------------

To install dop, simply: ::

    $ pip install dop


Example
-------
It is pretty easy to use: ::

    from dop.client import Client

    client = Client('client_id', 'api_key')
    regions = client.regions()
    for region in regions:
        print region



Contribute
----------
Pull requests and improvements are welcome.

.. _`here`: https://www.digitalocean.com/api

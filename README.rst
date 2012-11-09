DOP: Digital Ocean API Python Wrapper
=====================================

DOP is a MIT licensed Python wrapper for Digital Ocean's API.


Features
--------

Full support for all methods listed `here`_ except (they have weird behaviour):
    - reset_root_password
    - restore_droplet
    - destroy_image

Support for ssh is still experimental. Digital Ocean does not have full support for adding ssh keys neither edit them yet.

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

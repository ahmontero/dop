# -*- coding: utf-8 -*-

"""
dop.client
~~~~~~~~~~~~

This module implements the Digital Ocean API.

:license: MIT, see LICENSE for more details.

"""

import requests

API_HOST = 'api.digitalocean.com'
API_PORT = 80


class Droplet(object):
    def __init__(self, id, name, size_id, image_id, region_id, event_id,
        backups_active, status, ip_address):
        self.id = id
        self.name = name
        self.size_id = size_id
        self.image_id = image_id
        self.region_id = region_id
        self.event_id = event_id
        self.backups_active = backups_active
        self.status = status
        self.ip_address = ip_address

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        id = json.get('id', -1)
        name = json.get('name', '')
        size_id = json.get('size_id', -1)
        image_id = json.get('image_id', -1)
        region_id = json.get('region_id', -1)
        event_id = json.get('event_id', -1)
        backups_active = json.get('backups_active', -1)
        status = json.get('status', '')
        ip_address = json.get('ip_address', -1)
        droplet = Droplet(id, name, size_id, image_id, region_id, event_id,
            backups_active, status, ip_address)
        return droplet


class Snapshot(object):
    def __init__(self, name):
        self.name = name

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        name = json.get('name', '')
        snapshot = Snapshot(name)
        return snapshot


class Region(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        id = json.get('id', -1)
        name = json.get('name', '')
        region = Region(id, name)
        return region


class Image(object):
    def __init__(self, id, name, distribution):
        self.id = id
        self.name = name
        self.distribution = distribution

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        id = json.get('id', -1)
        name = json.get('name', '')
        distribution = json.get('distribution', '')
        image = Image(id, name, distribution)
        return image


class Size(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        id = json.get('id', -1)
        name = json.get('name', '')
        size = Size(id, name)
        return size


class SSHKey(object):
    def __init__(self, id, key):
        self.id = id
        self.key = key

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        id = json.get('id', -1)
        key = json.get('key', '')
        ssh_key = SSHKey(id, key)
        return ssh_key


class Client(object):

    def __init__(self, client_id, api_key, host=API_HOST, port=API_PORT,
        secure=True):
        self.client_id = client_id
        self.api_key = api_key
        self.host = host
        self.port = port
        self.secure = secure

    def show_active_droplets(self):
        params = {}
        json = self.request('/droplets', method='GET', params=params)
        droplets_json = json.get('droplets', [])
        droplets = [Droplet.from_json(s) for s in droplets_json]
        return droplets

    def regions(self):
        params = {}
        json = self.request('/regions', method='GET', params=params)
        regions_json = json.get('regions', [])
        regions = [Region.from_json(r) for r in regions_json]
        return regions

    def images(self, show_all=True):
        params = {}
        if show_all:
            params['filter'] = 'global'
        else:
            params['filter'] = 'my_images'

        json = self.request('/images', method='GET', params=params)
        images_json = json.get('images', [])
        images = [Image.from_json(i) for i in images_json]
        return images

    def sizes(self):
        params = {}
        json = self.request('/sizes', method='GET', params=params)
        sizes_json = json.get('sizes', [])
        sizes = [Size.from_json(s) for s in sizes_json]
        return sizes

    def all_ssh_keys(self):
        params = {}
        json = self.request('/ssh_keys', method='GET', params=params)
        ssh_keys_json = json.get('ssh_keys', [])
        sizes = [Size.from_json(k) for k in ssh_keys_json]
        return sizes

    def reboot_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/reboot' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    def show_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s' % (id), method='GET', params=params)
        droplet_json = json.get('droplet', None)
        droplet = Droplet.from_json(droplet_json)
        return droplet

    def create_droplet(self, name="", size_id=-1, image_id=-1, region_id=-1):
        params = {
            'name': name,
            'size_id': size_id,
            'image_id': image_id,
            'region_id': region_id,
        }
        json = self.request('/droplets/new', method='GET', params=params)
        droplet_json = json.get('droplet', None)
        droplet = Droplet.from_json(droplet_json)
        return droplet

    def power_cycle_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/power_cycle' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    def power_off_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/power_off' % (id), method='GET',
            params=params)
        return json.get('event_id', None)

    def power_on_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/power_on' % (id), method='GET',
            params=params)
        return json.get('event_id', None)

    def resize_droplet(self, id, size_id):
        params = {
            'size_id': size_id,
        }
        json = self.request('/droplets/%s/resize' % (id), method='POST',
            params=params)
        return json

    def snapshot_droplet(self, id, name):
        params = {
            'name': name,
        }
        json = self.request('/droplets/%s/snapshot' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    def rebuild_droplet(self, id, image_id):
        params = {
            'image_id': image_id,
        }
        json = self.request('/droplets/%s/rebuild' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    def enable_backups_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/enable_backups' % (id),
            method='POST', params=params)
        return json.get('event_id', None)

    def disable_backups_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/disable_backups' % (id),
            method='POST', params=params)
        return json.get('event_id', None)

    def destroy_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/destroy' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    def show_image(self, image_id):
        params = {
            'image_id': image_id,
        }
        json = self.request('/images/%s' % (image_id), method='GET',
            params=params)
        image_json = json.get('image', None)
        image = Image.from_json(image_json)
        return image

    def shutdown_droplet(self, id):
        params = {}
        json = self.request('/droplets/%s/shutdown' % (id), method='POST',
            params=params)
        return json.get('event_id', None)

    # WEIRD BEHAVIOUR METHODS
    def reset_root_password(self, id):
        params = {}
        json = self.request('/droplets/%s/reset_root_password' % (id),
            method='GET', params=params)
        print json
        return json.get('event_id', None)

    def restore_droplet(self, id, image_id):
        params = {
            'image_id': image_id,
        }
        json = self.request('/droplets/%s/restore' % (id), method='GET',
            params=params)
        print json
        return json.get('event_id', None)

    def destroy_image(self, image_id):
        params = {}
        json = self.request('/images/%s/destroy' % (image_id), method='GET',
            params=params)
        print json
        event = json.get('event', None)
        return event

    def show_ssh_key(self, id):
        params = {}
        json = self.request('/ssh_keys/%s' % (id), method='GET', params=params)
        ssh_key_json = json.get('ssh_key', None)
        ssh_key = SSHKey.from_json(ssh_key_json)
        return ssh_key

    def destroy_ssh_key(self, id):
        params = {}
        json = self.request('/ssh_keys/%s/destroy' % (id), method='GET',
            params=params)
        ssh_key = SSHKey.from_json(json)
        return ssh_key

    # EXPERIMENTAL: ssh actions #
    def add_ssh_key(self, id):
        params = {}
        json = self.request('/ssh_key/%s/add' % (id), method='GET',
            params=params)
        print json
        ssh_key_json = json.get('ssh_key', None)
        ssh_key = SSHKey.from_json(ssh_key_json)
        return ssh_key

    def edit_ssh_key(self, id):
        params = {}
        json = self.request('/ssh_key/%s/edit' % (id), method='GET',
            params=params)
        ssh_key = SSHKey.from_json(json)
        return ssh_key

    def request(self, target, method='GET', params={}):
        assert method in ['GET', 'POST'], \
            "Only 'GET' 'POST' are allowed."

        headers = {
            'User-Agent': 'dop/client'
        }

        params['client_id'] = self.client_id
        params['api_key'] = self.api_key

        if method == 'POST':
            headers['Content-Type'] = "application/json"
            url = self.get_url(target)
            response = requests.post(url, headers=headers, params=params)
        else:
            url = self.get_url(target)
            response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            if response.json():
                json = response.json()
                error_msg = json.get('error_message', None)
                if error_msg:
                    raise DOPException(error_msg)
                else:
                    return json
            else:
                raise DOPException('Empty json!')
        else:
            error = 'Status code: %d' % (response.status_code)
            raise DOPException(error)
        return json

    def get_url(self, slug):
        port = "" if self.port == 80 else ":%d" % self.port
        protocol = "https://" if self.secure else "http://"
        base_full_url = "%s%s%s%s" % (protocol, self.host, port, slug)
        return base_full_url


class DOPException(Exception):
    pass

# -*- coding: utf-8 -*-

"""
dop.client
~~~~~~~~~~~~

This module implements the Digital Ocean API.

:license: MIT, see LICENSE for more details.

"""

import requests

import __version__

API_HOST = 'api.digitalocean.com'
API_PORT = 80


class BaseObject(object):

    def to_json(self):
        res = dict()
        for k, v in self.__dict__.items():
            if v:
                res.update({k: v})
        return res


class Droplet(BaseObject):
    def __init__(self, droplet_id, name, image_id, size_id, region_id,
                 backups_active, ip_address, private_ip_address, locked, status,
                 created_at, backups, snapshots):
        self.droplet_id = droplet_id
        self.name = name
        self.size_id = size_id
        self.image_id = image_id
        self.region_id = region_id
        self.backups_active = backups_active
        self.ip_address = ip_address
        self.private_ip_address = private_ip_address
        self.locked = locked
        self.status = status
        self.created_at = created_at
        self.backups = backups
        self.snapshots = snapshots

    @staticmethod
    def from_json(json):
        droplet_id = json.get('id')
        name = json.get('name')
        image_id = json.get('image_id')
        size_id = json.get('size_id')
        region_id = json.get('region_id')
        backups_active = json.get('backups_active')
        ip_address = json.get('ip_address')
        private_ip_address = json.get('private_ip_address')
        locked = json.get('locked')
        status = json.get('status')
        created_at = json.get('created_at')
        backups = json.get('backups')
        snapshots = json.get('snapshots')

        droplet = Droplet(droplet_id, name, image_id, size_id, region_id,
                          backups_active, ip_address, private_ip_address,
                          locked, status, created_at, backups, snapshots)
        return droplet


class Event(BaseObject):
    def __init__(self, event_id, action_status, droplet_id, event_type_id, percentage):
        self.event_id = event_id
        self.action_status = action_status
        self.droplet_id = droplet_id
        self.event_type_id = event_type_id
        self.percentage = percentage

    @staticmethod
    def from_json(json):
        event_id = json.get('id')
        action_status = json.get('action_status')
        droplet_id = json.get('droplet_id')
        event_type_id = json.get('event_type_id')
        percentage = json.get('percentage')
        event = Event(event_id, action_status, droplet_id, event_type_id, percentage)
        return event


class Snapshot(BaseObject):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def from_json(json):
        name = json.get('name', '')
        snapshot = Snapshot(name)
        return snapshot


class Region(BaseObject):
    def __init__(self, region_id, name, slug):
        self.region_id = region_id
        self.name = name
        self.slug = slug

    @staticmethod
    def from_json(json):
        region_id = json.get('id')
        name = json.get('name')
        slug = json.get('slug')
        region = Region(region_id, name, slug)
        return region


class Image(BaseObject):
    def __init__(self, image_id, name, distribution, slug, public):
        self.image_id = image_id
        self.name = name
        self.slug = slug
        self.distribution = distribution
        self.public = public

    @staticmethod
    def from_json(json):
        image_id = json.get('id')
        name = json.get('name')
        distribution = json.get('distribution')
        slug = json.get('slug')
        public = json.get('public')
        image = Image(image_id, name, distribution, slug, public)
        return image


class Size(BaseObject):
    def __init__(self, size_id, name, slug):
        self.size_id = size_id
        self.name = name
        self.slug = slug

    @staticmethod
    def from_json(json):
        size_id = json.get('id')
        name = json.get('name')
        slug = json.get('slug')
        size = Size(size_id, name, slug)
        return size


class SSHKey(BaseObject):
    def __init__(self, ssh_key_id, name, ssh_pub_key):
        self.ssh_key_id = ssh_key_id
        self.name = name
        self.ssh_pub_key = ssh_pub_key

    @staticmethod
    def from_json(json):
        ssh_key_id = json.get('id')
        name = json.get('name')
        ssh_pub_key = json.get('ssh_pub_key')
        ssh_key = SSHKey(ssh_key_id, name, ssh_pub_key)
        return ssh_key


class Domain(BaseObject):
    def __init__(self, domain_id, name, ttl, live_zone_file, error, zone_file_with_error):
        self.domain_id = domain_id
        self.name = name
        self.ttl = ttl
        self.live_zone_file = live_zone_file
        self.error = error
        self.zone_file_with_error = zone_file_with_error

    @staticmethod
    def from_json(json):
        domain_id = json.get('id')
        name = json.get('name')
        ttl = json.get('ttl')
        live_zone_file = json.get('live_zone_file')
        error = json.get('error')
        zone_file_with_error = json.get('zone_file_with_error')
        domain = Domain(domain_id, name, ttl, live_zone_file, error, zone_file_with_error)
        return domain


class Record(BaseObject):
    def __init__(self, record_id, domain_id, record_type, name, data, priority,
                 port, weight):
        self.record_id = record_id
        self.domain_id = domain_id
        self.record_type = record_type
        self.name = name
        self.data = data
        self.priority = priority
        self.port = port
        self.weight = weight

    @staticmethod
    def from_json(json):
        record_id = json.get('id')
        domain_id = json.get('domain_id')
        record_type = json.get('record_type')
        name = json.get('name')
        data = json.get('data')
        priority = json.get('priority')
        port = json.get('port')
        weight = json.get('weight')
        record = Record(record_id, domain_id, record_type, name, data, priority,
                        port, weight)
        return record


class Client(object):

    def __init__(self, client_id, api_key, host=API_HOST, port=API_PORT,
                 secure=True):
        self.client_id = client_id
        self.api_key = api_key
        self.host = host
        self.port = port
        self.secure = secure

    def create_droplet(self, name=None, size=None, image=None, region=None,
                       ssh_key_ids=None, virtio=False, private_networking=False,
                       backups_enabled=False):
        """


        Required parameters:

            name: String, this is the name of the droplet - must be formatted
                  by hostname rules

            size, one of
                size_id: Numeric, this is the id of the size with which you
                         would like the droplet created
                size_slug: String, this is the slug of the size with which you
                           would like the droplet created
            image, one of
                image_id: Numeric, this is the id of the image you would like
                          the droplet created with
                image_slug: String, this is the slug of the image you would like
                            the droplet created with
            region, one of
                region_id: Numeric, this is the id of the region you would like
                           your server in
                region_slug: String, this is the slug of the region you would
                             like your server in

        Optional parameters:

            ssh_key_ids: Numeric CSV, comma separated list of ssh_key_ids that
                         you would like to be added to the server

            private_networking: Boolean, enables a private network interface if
                                the region supports private networking

            backups_enabled: Boolean, enables backups for your droplet.

        """
        if not name:
            raise DOPException('name is required to create a droplet!')
        params = dict(name=name, virtio=virtio, private_networking=private_networking,
                      backups_enabled=backups_enabled)
        if ssh_key_ids:
            params['ssh_key_ids'] = ','.join(ssh_key_ids)

        size_id = size.get('size_id')
        if size_id:
            params.update({'size_id': size_id})
        else:
            size_slug = size.get('size_slug')
            if size_slug:
                params.update({'size_slug': size_slug})
            else:
                raise DOPException('size_id or size_slug are required to create a droplet!')

        image_id = image.get('image_id')
        if image_id:
            params.update({'image_id': image_id})
        else:
            image_slug = size.get('image_slug')
            if image_slug:
                params.update({'image_slug': image_slug})
            else:
                raise DOPException('image_id or image_slug are required to create a droplet!')

        region_id = region.get('region_id')
        if image_id:
            params.update({'region_id': region_id})
        else:
            region_slug = size.get('region_slug')
            if region_slug:
                params.update({'region_slug': region_slug})
            else:
                raise DOPException('region_id or region_slug are required to create a droplet!')

        json = self.request('/droplets/new', method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            droplet_json = json.get('droplet', None)
            droplet = Droplet.from_json(droplet_json)
            return droplet
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def show_droplet(self, droplet_id):
        """
        This method returns full information for a specific droplet ID that is
        passed in the URL.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to show a droplet!')
        json = self.request('/droplets/%s' % droplet_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            droplet_json = json.get('droplet', None)
            droplet = Droplet.from_json(droplet_json)
            return droplet
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def reboot_droplet(self, droplet_id):
        """
        This method allows you to reboot a droplet. This is the preferred method
        to use if a server is not responding.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to reboot a droplet!')
        json = self.request('/droplets/%s/reboot' % droplet_id, method='POST')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def power_cycle_droplet(self, droplet_id):
        """
        This method allows you to power cycle a droplet. This will turn off the
        droplet and then turn it back on.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to power cycle a droplet!')
        json = self.request('/droplets/%s/power_cycle' % droplet_id, method='POST')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def shutdown_droplet(self, droplet_id):
        """
        This method allows you to shutdown a running droplet. The droplet will
        remain in your account.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to shutdown a droplet!')
        json = self.request('/droplets/%s/shutdown' % droplet_id, method='POST')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def power_off_droplet(self, droplet_id):
        """
        This method allows you to poweroff a running droplet. The droplet will
        remain in your account.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to power off a droplet!')
        json = self.request('/droplets/%s/power_off' % droplet_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def power_on_droplet(self, droplet_id):
        """
        This method allows you to poweron a powered off droplet.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to power on a droplet!')
        json = self.request('/droplets/%s/power_on' % droplet_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def password_reset(self, droplet_id):
        """
        This method will reset the root password for a droplet. Please be aware
        that this will reboot the droplet to allow resetting the password.
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to reset password on a droplet!')
        json = self.request('/droplets/%s/password_reset' % droplet_id,
                            method='GET')
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def resize_droplet(self, droplet_id, size):
        """
        This method allows you to resize a specific droplet to a different size.
        This will affect the number of processors and memory allocated to the droplet.

        Required parameters:

            droplet_id:
                Integer, this is the id of your droplet that you want to resize

            size, one of
                size_id: Numeric, this is the id of the size with which you
                         would like the droplet created
                size_slug: String, this is the slug of the size with which you
                           would like the droplet created
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to resize a droplet!')
        params = {}
        size_id = size.get('size_id')
        if size_id:
            params.update({'size_id': size_id})
        else:
            size_slug = size.get('size_slug')
            if size_slug:
                params.update({'size_slug': size_slug})
            else:
                msg = 'size_id or size_slug are required to resize a droplet!'
                raise DOPException(msg)

        json = self.request('/droplets/%s/resize' % droplet_id, method='POST',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def snapshot_droplet(self, droplet_id, name):
        """
        This method allows you to take a snapshot of the droplet once it has been
        powered off, which can later be restored or used to create a new droplet
        from the same image. Please be aware this may cause a reboot.

        Required parameters:

            droplet_id:
                Numeric, this is the id of your droplet that you want to snapshot

        Optional parameters:

            name:
                String, this is the name of the new snapshot you want to create.
                If not set, the snapshot name will default to date/time
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to snapshot a droplet!')
        params = {'name': name}
        json = self.request('/droplets/%s/snapshot' % id, method='POST',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def restore_droplet(self, droplet_id, image_id):
        """
        This method allows you to restore a droplet with a previous image or snapshot.
        This will be a mirror copy of the image or snapshot to your droplet.
        Be sure you have backed up any necessary information prior to restore.

        Required parameters:

            droplet_id:
                Numeric, this is the id of your droplet that you want to snapshot

            image_id:
                Numeric, this is the id of the image you would like to use to
                restore your droplet with
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to restore a droplet!')
        if not image_id:
            raise DOPException('image_id is required to rebuild a droplet!')
        params = {'image_id': image_id}
        json = self.request('/droplets/%s/restore' % id, method='GET',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def rebuild_droplet(self, droplet_id, image_id):
        """
        This method allows you to reinstall a droplet with a default image.
        This is useful if you want to start again but retain the same IP address
        for your droplet.

        Required parameters:

            droplet_id:
                Numeric, this is the id of your droplet that you want to snapshot

            image_id:
                Numeric, this is the id of the image you would like to use to
                rebuild  your droplet with
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to rebuild a droplet!')
        if not image_id:
            raise DOPException('image_id is required to rebuild a droplet!')
        params = {
            'image_id': image_id,
        }
        json = self.request('/droplets/%s/rebuild' % id, method='POST',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def rename_droplet(self, droplet_id, name):
        """
        This method allows you to reinstall a droplet with a default image.
        This is useful if you want to start again but retain the same IP address
        for your droplet.

        Required parameters:

            droplet_id:
                Numeric, this is the id of your droplet that you want to snapshot

            image_id:
                Numeric, this is the id of the image you would like to use to
                rebuild  your droplet with
        """
        if not droplet_id:
            raise DOPException('droplet_id is required to rebuild a droplet!')
        if not name:
            raise DOPException('name is required to rebuild a droplet!')
        params = {'name': name}
        json = self.request('/droplets/%s/rename' % id, method='GET',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def destroy_droplet(self, droplet_id, scrub_data=False):
        """
        This method destroys one of your droplets - this is irreversible.

        Required parameters:

            droplet_id:
                Numeric, this is the id of your droplet that you want to destroy

        Optional parameters

            scrub_data:
                Boolean, this will strictly write 0s to your prior partition to
                ensure that all data is completely erased
        """
        params = {}

        if scrub_data:
            params['scrub_data'] = True

        json = self.request('/droplets/%s/destroy' % droplet_id, method='GET',
                            params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def regions(self):
        """
        This method will return all the available regions within the
        DigitalOcean cloud.
        """
        json = self.request('/regions', method='GET')
        status = json.get('status')
        if status == 'OK':
            regions_json = json.get('regions', [])
            regions = [Region.from_json(region) for region in regions_json]
            return regions
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def images(self, filter='my_images'):
        """
        This method returns all the available images that can be accessed by
        your client ID. You will have access to all public images by default,
        and any snapshots or backups that you have created in your own account.

        Optional parameters

            filter:
                String, either "my_images" or "global"
        """
        if filter and filter not in ('my_images', 'global'):
            raise DOPException('"filter" must be either "my_images" or "global"')
        params = {}
        if filter:
            params['filter'] = filter
        json = self.request('/images', method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            images_json = json.get('images', [])
            images = [Image.from_json(image) for image in images_json]
            return images
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def show_image(self, image_id_or_slug):
        """
        This method displays the attributes of an image.

        Required parameters

            image_id:
                Numeric, this is the id of the image you would like to use to
                rebuild your droplet with
        """
        if not image_id_or_slug:
            raise DOPException('image_id_or_slug is required to destroy an image!')

        json = self.request('/images/%s' % image_id_or_slug, method='GET')
        image_json = json.get('image', None)
        status = json.get('status')
        if status == 'OK':
            image = Image.from_json(image_json)
            return image
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def destroy_image(self, image_id_or_slug):
        """
        This method allows you to destroy an image. There is no way to restore
        a deleted image so be careful and ensure your data is properly backed up.

        Required parameters

            image_id:
                Numeric, this is the id of the image you would like to destroy
        """

        if not image_id_or_slug:
            raise DOPException('image_id_or_slug is required to destroy an image!')

        json = self.request('/images/%s/destroy' % image_id_or_slug, method='GET')
        status = json.get('status')
        return status

    def transfer_image(self, image_id_or_slug, region_id):
        """
        This method allows you to transfer an image to a specified region.

        Required parameters

            image_id:
                Numeric, this is the id of the image you would like to transfer.

            region_id
                Numeric, this is the id of the region to which you would like to transfer.
        """
        if not image_id_or_slug:
            raise DOPException('image_id_or_slug is required to transfer an image!')

        if not region_id:
            raise DOPException('region_id is required to transfer an image!')
        params = {'region_id': region_id}
        json = self.request('/images/%s/transfer' % image_id_or_slug,
                            method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            return json.get('event_id')
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def ssh_keys(self):
        """
        This method lists all the available public SSH keys in your account
        that can be added to a droplet.
        """
        params = {}
        json = self.request('/ssh_keys', method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            ssh_keys_json = json.get('ssh_keys', [])
            keys = [SSHKey.from_json(ssh_key) for ssh_key in ssh_keys_json]
            return keys
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def add_ssh_key(self, name, ssh_pub_key):
        """
        This method allows you to add a new public SSH key to your account.

        Required parameters

            name:
                String, the name you want to give this SSH key.

            ssh_pub_key:
                String, the actual public SSH key.
        """
        params = {'name': name, 'ssh_pub_key': ssh_pub_key}
        json = self.request('/ssh_keys/new' % id, method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            ssh_key_json = json.get('ssh_key', None)
            ssh_key = SSHKey.from_json(ssh_key_json)
            return ssh_key
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def show_ssh_key(self, ssh_key_id):
        """
        This method shows a specific public SSH key in your account that can be
        added to a droplet.
        """
        params = {}
        json = self.request('/ssh_keys/%s' % ssh_key_id, method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            ssh_key_json = json.get('ssh_key', None)
            ssh_key = SSHKey.from_json(ssh_key_json)
            return ssh_key
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def edit_ssh_key(self, ssh_key_id, ssh_pub_key):
        """
        This method allows you to modify an existing public SSH key in your account.
        """
        params = {'ssh_pub_key': ssh_pub_key}
        json = self.request('/ssh_keys/%s/edit' % ssh_key_id, method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            ssh_key_json = json.get('ssh_key', None)
            ssh_key = SSHKey.from_json(ssh_key_json)
            return ssh_key
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def destroy_ssh_key(self, ssh_key_id):
        """
        This method will delete the SSH key from your account.
        """
        json = self.request('/ssh_keys/%s/destroy' % ssh_key_id, method='GET')
        status = json.get('status')
        return status

    def sizes(self):
        """
        This method returns all the available sizes that can be used to create
        a droplet.
        """
        json = self.request('/sizes', method='GET')
        status = json.get('status')
        if status == 'OK':
            sizes_json = json.get('sizes', [])
            sizes = [Size.from_json(s) for s in sizes_json]
            return sizes
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def domains(self):
        """
        This method returns all of your current domains.
        """
        json = self.request('/domains', method='GET')
        status = json.get('status')
        if status == 'OK':
            domains_json = json.get('domains', [])
            domains = [Domain.from_json(domain) for domain in domains_json]
            return domains
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def create_domain(self, name, ip_address):
        """
        This method creates a new domain name with an A record for the specified [ip_address].

        Required parameters

            name:
                String, the name you want to give this SSH key.

            ip_address:
                String, ip address for the domain's initial a record.
        """
        params = {'name': name, 'ip_address': ip_address}
        json = self.request('/domains/new', method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            domain_json = json.get('domain')
            domain = Domain.from_json(domain_json)
            return domain
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def show_domain(self, domain_id):
        """
        This method returns the specified domain.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                to display.
        """
        json = self.request('/domains/%s' % domain_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            domain_json = json.get('domain')
            domain = Domain.from_json(domain_json)
            return domain
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def destroy_domain(self, domain_id):
        """
        This method deletes the specified domain.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                to destroy.
        """
        json = self.request('/domains/%s/destroy' % domain_id, method='GET')
        status = json.get('status')
        return status

    def domain_records(self, domain_id):
        """
        This method returns all of your current domain records.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                for which to retrieve records.
        """
        json = self.request('/domains/%s/records' % domain_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            records_json = json.get('records', [])
            records = [Record.from_json(record) for record in records_json]
            return records
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def create_domain_record(self, domain_id, record_type, data, name=None,
                             priority=None, port=None, weight=None):
        """
        This method creates a new domain name with an A record for the specified
        [ip_address].

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                for which to create a record.

            record_type:
                String, the type of record you would like to create.
                'A', 'CNAME', 'NS', 'TXT', 'MX' or 'SRV'

            data:
                String, this is the value of the record

        Optional parameters
            name:
                String, required for 'A', 'CNAME', 'TXT' and 'SRV' records

            priority:
                Integer, required for 'SRV' and 'MX' records

            port:
                Integer, required for 'SRV' records

            weight:
                Integer, required for 'SRV' records
        """
        params = dict(record_type=record_type, data=data)

        if name:
            params.update({'name': name})
        if priority:
            params.update({'priority': priority})
        if port:
            params.update({'port': port})
        if weight:
            params.update({'weight': weight})

        json = self.request('/domains/%s/records/new' % domain_id, method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            domain_record_json = json.get('domain_record')
            domain_record = Record.from_json(domain_record_json)
            return domain_record
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def show_domain_record(self, domain_id, record_id):
        """
        This method returns the specified domain record.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                for which to retrieve a record.

            record_id:
                Integer, specifies the record_id to retrieve.
        """
        json = self.request('/domains/%s/records/%s' % (domain_id, record_id),
                            method='GET')
        status = json.get('status')
        if status == 'OK':
            domain_record_json = json.get('record')
            domain_record = Record.from_json(domain_record_json)
            return domain_record
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def create_domain_record(self, domain_id, record_id, record_type, data,
                             name=None, priority=None, port=None, weight=None):
        """
        This method edits an existing domain record.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                for which to create a record.

            record_id:
                Integer, specifies the record to update.

            record_type:
                String, the type of record you would like to create.
                'A', 'CNAME', 'NS', 'TXT', 'MX' or 'SRV'

            data:
                String, this is the value of the record.

        Optional parameters
            name:
                String, required for 'A', 'CNAME', 'TXT' and 'SRV' records

            priority:
                Integer, required for 'SRV' and 'MX' records

            port:
                Integer, required for 'SRV' records

            weight:
                Integer, required for 'SRV' records
        """
        params = dict(record_type=record_type, data=data)

        if name:
            params.update({'name': name})
        if priority:
            params.update({'priority': priority})
        if port:
            params.update({'port': port})
        if weight:
            params.update({'weight': weight})

        json = self.request('/domains/%s/records/%s/edit' % (domain_id, record_id),
                            method='GET', params=params)
        status = json.get('status')
        if status == 'OK':
            domain_record_json = json.get('record')
            domain_record = Record.from_json(domain_record_json)
            return domain_record
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def destroy_domain_record(self, domain_id, record_id):
        """
        This method deletes the specified domain record.

        Required parameters

            domain_id:
                Integer or Domain Name (e.g. domain.com), specifies the domain
                for which to destroy a record.

            record_id:
                Integer, specifies the record_id to destroy.
        """
        json = self.request('/domains/%s/records/%s/destroy' % (domain_id, record_id),
                            method='GET')
        status = json.get('status')
        return status

    def events(self, event_id):
        """
        This method is primarily used to report on the progress of an event
        by providing the percentage of completion.

        Required parameters

            event_id:
                Numeric, this is the id of the event you would like more
                information about
        """
        json = self.request('/events/%s' % event_id, method='GET')
        status = json.get('status')
        if status == 'OK':
            event_json = json.get('event', None)
            event = Event.from_json(event_json)
            return event
        else:
            message = json.get('message', None)
            raise DOPException('[%s]: %s' % (status, message))

    def request(self, target, method='GET', params={}):
        assert method in ['GET', 'POST'], \
            "Only 'GET' or 'POST' are allowed."

        headers = {
            'User-Agent': 'dop/client v.%s' % __version__
        }

        params['client_id'] = self.client_id
        params['api_key'] = self.api_key
        url = self.get_url(target)
        if method == 'POST':
            headers['Content-Type'] = "application/json"
            response = requests.post(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response_json = response.json()
            if response_json:
                error_msg = response_json.get('error_message')
                if error_msg:
                    raise DOPException(error_msg)
                else:
                    return response_json
            else:
                raise DOPException(response)
        else:
            error = ('Status code: %d, full response: %s' %
                     (response.status_code, response.json()))
            raise DOPException(error)

    def get_url(self, slug):
        port = "" if self.port == 80 else ":%d" % self.port
        protocol = "https://" if self.secure else "http://"
        base_full_url = "%s%s%s%s" % (protocol, self.host, port, slug)
        return base_full_url


class DOPException(Exception):
    pass

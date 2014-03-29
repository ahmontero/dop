# -*- coding: utf-8 -*-


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

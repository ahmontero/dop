# purpose is to save password user credentials for later use in config file
import json
import os
import textwrap
import getpass

from binascii import hexlify, unhexlify as hex2bin
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import new as srand

bin2hex = lambda i: hexlify(i).decode('utf8')


class Credentials:
    def __init__(self, filename):
        self.filename = filename
        self.client_id = None
        self.api_key = None

    def available(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename, 'r') as f:
            data = json.loads(f.read())
            for i in range(0, 3):
                password = getpass.getpass(
                    'Password to restore Digital Ocean credentials: ')
                try:
                    (self.client_id, self.api_key) = self.decrypt(data, password)
                    break
                except UnicodeDecodeError:
                    print("bad password.", 2 - i, "retries left")
        if self.client_id is None or self.api_key is None:
            raise RuntimeError(
                'Failed to decrypt Digital Ocean credentials: bad password')

    def input(self):
        print(textwrap.dedent("""\
        Every API call needs Client Id and API Key.
        This credentials could be obtained here: https://cloud.digitalocean.com/api_access
        """))
        self.client_id = input("Please enter DO Client Id: ")
        self.api_key = input("Please enter DO API Key: ")

    def get(self):
        return self.client_id, self.api_key

    def save(self):
        with open(self.filename, 'w') as f:
            print("You're going to store Digital Ocean credentials in file: ",
                  self.filename)
            password = getpass.getpass("Please enter encryption password: ")
            f.write(self.encrypt(self.client_id, self.api_key, password))

    def makeKey(self, password, salt):
        salt_hash = SHA256.new()
        salt_hash.update(salt)
        pass_hash = SHA256.new()
        pass_hash.update(salt_hash.hexdigest().encode('utf8'))
        pass_hash.update(password.encode('utf8'))
        return pass_hash.digest()

    def encrypt(self, client_id, api_key, password):
        rand = srand()
        salt = rand.read(32)
        iv = rand.read(AES.block_size)
        key = self.makeKey(password, salt)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        encdata = cipher.encrypt(json.dumps([client_id, api_key]).encode('utf8'))
        return json.dumps([bin2hex(salt), bin2hex(iv), bin2hex(encdata)])

    def decrypt(self, file_json_data, password):
        salt = hex2bin(file_json_data[0])
        iv = hex2bin(file_json_data[1])
        encdata = hex2bin(file_json_data[2])
        key = self.makeKey(password, salt)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        decdata = cipher.decrypt(encdata).decode('utf8')
        return tuple(json.loads(decdata))

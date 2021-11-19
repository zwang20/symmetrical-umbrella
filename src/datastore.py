"""
datastore.py

contains the DataStore class
"""

import json
import logging
import os
import sys

import rsa


class DataStore:
    """
    DataStore

    The DataStore class is used to store data.
    """

    initial_data = {}


    def __init__(self):
        """
        __init__

        Initializes the DataStore.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())
        
        # check if ./data/ directory exists
        data_path = os.path.join(current_path, 'data')
        if not os.path.exists(data_path):
            logging.info('Creating ./data/ directory')
            os.makedirs(data_path)

        # check if data/data.json exists
        data_file_path = os.path.join(data_path, 'data.json')
        if not os.path.exists(data_file_path):
            logging.info('Creating data/data.json')
            with open(data_file_path, 'wb') as data_file:
                json.dump(self.initial_data, data_file)

        # check if ./data/keys/ directory exists
        keys_path = os.path.join(data_path, 'keys')
        if not os.path.exists(keys_path):
            logging.info('Creating ./data/keys/ directory')
            os.makedirs(keys_path)

        # check if ./data/keys/key exists
        key_file_path = os.path.join(keys_path, 'key.pub')
        if not os.path.exists(key_file_path):
            logging.info('Creating ./data/keys/key.pub')
            self.reset_keys()


    def get(self):
        """
        get

        Gets the data.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get data path
        data_path = os.path.join(current_path, 'data')

        # get data file path
        data_file_path = os.path.join(data_path, 'data.json')

        # get data
        with open(data_file_path, 'rb') as data_file:
            data = json.load(data_file)

        # return data
        return data


    def set(self, data):
        """
        set

        Sets the data.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get data path
        data_path = os.path.join(current_path, 'data')

        # get data file path
        data_file_path = os.path.join(data_path, 'data.json')

        # set data
        with open(data_file_path, 'wb') as data_file:
            json.dump(data, data_file)


    def _generate_keys(self):
        """
        _generate_keys

        Generates the keys.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get data path
        data_path = os.path.join(current_path, 'data')

        # get keys path
        keys_path = os.path.join(data_path, 'keys')

        # generate keys
        public_key, private_key = rsa.newkeys(2048)

        # store public key
        with open(os.path.join(keys_path, 'key.pub'), 'wb') as key_file:
            key_file.write(public_key.save_pkcs1())

        # store private key
        with open(os.path.join(keys_path, 'key'), 'wb') as key_file:
            key_file.write(private_key.save_pkcs1())


    def reset_keys(self):
        """
        reset_keys

        Resets the keys.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get data path
        data_path = os.path.join(current_path, 'data')

        # get keys path
        keys_path = os.path.join(data_path, 'keys')

        # get key file paths
        public_key_file_path = os.path.join(keys_path, 'key.pub')
        private_key_file_path = os.path.join(keys_path, 'key')

        # delete public key
        if os.path.exists(public_key_file_path):
            os.remove(public_key_file_path)

        # delete private key
        if os.path.exists(private_key_file_path):
            os.remove(private_key_file_path)

        # generate keys
        self._generate_keys()


    def get_keys(self):
        """
        get_keys

        Gets the keys.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get data path
        data_path = os.path.join(current_path, 'data')

        # get keys path
        keys_path = os.path.join(data_path, 'keys')

        # get key file paths
        public_key_file_path = os.path.join(keys_path, 'key.pub')
        private_key_file_path = os.path.join(keys_path, 'key')

        # get public key
        with open(public_key_file_path, 'rb') as key_file:
            public_key = rsa.PublicKey.load_pkcs1(key_file.read())

        # get private key
        with open(private_key_file_path, 'rb') as key_file:
            private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

        # return keys
        return (public_key, private_key)


    def get_root_key(self):
        """
        get_root_key

        Gets the root key.
        """

        # get current path
        current_path = os.path.dirname(os.getcwd())

        # get root key path
        root_key_file_path = os.path.join(current_path, 'root_key.pub')

        # check if root key exists
        if not os.path.exists(root_key_file_path):
            logging.critical('Root key does not exist')
            sys.exit(1)

        # get root key
        with open(root_key_file_path, 'rb') as key_file:
            root_key = rsa.PublicKey.load_pkcs1(key_file.read())

        # return root key
        return root_key

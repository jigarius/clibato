"""Clibato Configuration"""

import typing
import yaml
from collections import deque

from .content import Content
from .destination import Destination


class Config:
    _DEFAULT = {
        'settings': {
            'workdir': '~/.clibato'
        },
        'contents': {},
        'destination': None
    }

    def __init__(self, data: dict):
        self._data = data
        self._workdir = None
        self._contents = None
        self._destination = None
        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.settings() == other.settings() and
            self.contents() == other.contents() and
            self.destination() == other.destination()
        )

    def settings(self):
        return self._get('settings')

    def workdir(self):
        if not self._workdir:
            self._workdir = self._get('settings.workdir')

        return self._workdir

    def contents(self):
        if not self._contents:
            data = self._get('contents')
            for destination in data:
                data[destination] = Content(destination, data[destination])
            self._contents = data

        return self._contents

    def destination(self):
        if not self._destination:
            dest_data = self._get('destination')
            self._destination = Destination.from_dict(dest_data)

        return self._destination

    def _validate(self):
        extra_keys = self._data.keys() - self._DEFAULT.keys()
        if len(extra_keys) != 0:
            extra_keys = list(extra_keys)
            extra_keys.sort()
            extra_keys = ', '.join(extra_keys)
            raise ConfigError(f'Illegal keys: {extra_keys}')

        if self.workdir() == '':
            raise ConfigError('Key cannot be empty: settings.workdir')

        if len(self.contents()) == 0:
            raise ConfigError('Key cannot be empty: contents')

        if not self._data.get('destination', None):
            raise ConfigError('Key cannot be empty: destination')

    def _get(self, key: str):
        value = self.extract(self._data, key)
        if value:
            return value

        return self.extract(self._DEFAULT, key)

    @staticmethod
    def extract(data: dict, key: str):
        key_parts = deque(key.split('.'))
        result = data

        while len(key_parts) != 0:
            cur_key = key_parts.popleft()

            if not isinstance(result, dict):
                return None

            if cur_key not in result:
                return None

            result = result[cur_key]

        return result

    @staticmethod
    def from_file(path):
        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError(str(error))

        return Config(data)


class ConfigError(KeyError):
    pass

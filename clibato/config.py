"""Clibato Configuration"""

from collections import deque
from typing import List
import os
import yaml

from .content import Content
from .destination import Destination


class Config:
    """Clibato Configuration"""
    _DEFAULT = {
        'settings': {
            'workdir': '~/.clibato'
        },
        'contents': {},
        'destination': None
    }

    def __init__(self, data: dict):
        self._data = Config.merge(self._DEFAULT, data)
        self._contents = None
        self._destination = None

        self._validate()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self)) and
            self.data() == other.data()
        )

    def data(self):
        """Get the underlying configuration as a dictionary"""
        return {**self._data}

    def workdir(self) -> str:
        """Get the working directory."""
        return self._data['settings']['workdir']

    def contents(self) -> List[Content]:
        """Get the contents, i.e. items to backup/restore."""
        if not self._contents:
            raw_contents = self._data['contents']
            self._contents = {}
            for backup_path in raw_contents:
                self._contents[backup_path] = Content(backup_path, raw_contents[backup_path])

        return self._contents

    def destination(self):
        """Get the destination configuration."""
        if not self._destination:
            self._destination = Destination.from_dict(self._data['destination'])

        return self._destination

    def _validate(self) -> type(None):
        extra_keys = self._data.keys() - self._DEFAULT.keys()
        if len(extra_keys) != 0:
            extra_keys = list(extra_keys)
            extra_keys.sort()
            extra_keys = ', '.join(extra_keys)
            raise ConfigError(f'Illegal keys: {extra_keys}')

        if not self._data['settings']['workdir']:
            raise ConfigError('Key cannot be empty: settings.workdir')

        if not self._data['contents']:
            raise ConfigError('Key cannot be empty: contents')

        if not self._data['destination']:
            raise ConfigError('Key cannot be empty: destination')

    @staticmethod
    def merge(dict1: dict, dict2: dict):
        """Create a dictionary where dict2 is merged into dict1"""
        result = {**dict1}

        for key in dict2:
            if key in result:
                # Merge dictionaries.
                if isinstance(result[key], dict) and isinstance(dict2[key], dict):
                    result[key] = Config.merge(result[key], dict2[key])
                    continue

                # Do not overwrite with non-empty strings.
                if isinstance(dict2[key], str) and dict2[key] == '':
                    continue

            result[key] = dict2[key]

        return result

    @staticmethod
    def extract(data: dict, key: str):
        """
        Extracts a key of the form "foo.bar" from the a dictionary.
        """
        key_parts = deque(key.split('.'))
        result = {**data}

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
        """Create Config object from a YAML file."""
        if path.startswith('~/'):
            path = os.path.expanduser(path)

        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError from error

        return Config(data)


class ConfigError(KeyError):
    """Configuration Error"""

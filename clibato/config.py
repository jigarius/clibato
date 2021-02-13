"""Clibato Configuration"""

from typing import List
import os
import yaml

from . import utils
from .error import ConfigError
from .content import Content
from .destination import Destination


class ConfigAbstract:
    """Configuration Abstract"""

    _DEFAULTS = {}

    def __init__(self, data: dict):
        self._data = utils.dict_merge(self._DEFAULTS, data)

        self._validate()

    def data(self):
        """Get the underlying config as a dictionary"""
        return {**self._data}

    def _validate(self):
        """Validates the config object at instantiation"""
        Config.ensure_shape(self._data, self._DEFAULTS)


class Config(ConfigAbstract):
    """Clibato Configuration"""

    _DEFAULTS = {
        'contents': {},
        'destination': {}
    }

    def __init__(self, data: dict):
        super().__init__(data)

        self._contents = None
        self._destination = None

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self)) and
            self.data() == other.data()
        )

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
        super()._validate()

        if not self._data['contents']:
            raise ConfigError('Key cannot be empty: contents')

        if not self._data['destination']:
            raise ConfigError('Key cannot be empty: destination')

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

    @staticmethod
    def ensure_shape(data: dict, shape: dict, parents=None) -> bool:
        """
        Checks keys in 'data' conform with the ones in 'shape'.

        An error is raised if:
          - data is missing a key that exists in shape.
          - data has a key that shape doesn't have.

        :param data: A dictionary.
        :param shape: A dictionary with the expected shape.
        :param parents: The parent key (for internal use).
        """
        parents = parents or []

        extra_keys = list(data.keys() - shape.keys())
        if extra_keys:
            extra_keys.sort()
            keys = map(lambda k: '.'.join([*parents, k]), extra_keys)
            keys = ', '.join(keys)
            raise ConfigError(f'Config has illegal keys: {keys}')

        missing_keys = list(shape.keys() - data.keys())
        if missing_keys:
            missing_keys.sort()
            keys = map(lambda k: '.'.join([*parents, k]), missing_keys)
            keys = ', '.join(keys)
            raise ConfigError(f'Config has missing keys: {keys}')

        for key in shape:
            if not isinstance(shape[key], dict):
                continue

            if len(shape[key]) == 0:
                continue

            if not isinstance(data[key], dict):
                key = '.'.join([*parents, key])
                raise ConfigError(f'Config must have keyed-values: #{key}')

            Config.ensure_shape(shape[key], data[key], [*parents, key])

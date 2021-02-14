"""Clibato Configuration"""

import os
from typing import List, Optional
import yaml

from .error import ConfigError
from .logger import Logger
from .content import Content
from .destination import Destination


class Config:
    """Clibato Configuration"""

    DEFAULT_FILENAME = '.clibato.yml'

    def __init__(self, contents: List[Content], destination: Destination):
        self._contents = contents
        self._destination = destination

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self)) and
            self.contents() == other.contents() and
            self.destination() == other.destination()
        )

    def contents(self) -> List[Content]:
        """Get the contents, i.e. items to backup/restore."""
        return self._contents

    def destination(self) -> Destination:
        """Get the destination configuration."""
        return self._destination

    @staticmethod
    def from_dict(data: dict):
        """
        Create Config object from a dictionary.

        :except ConfigError
        """
        required_keys = ['contents', 'destination']

        extra_keys = list(data.keys() - required_keys)
        if extra_keys:
            extra_keys.sort()
            raise ConfigError('Config has illegal keys: %s' % ', '.join(extra_keys))

        missing_keys = list(required_keys - data.keys())
        if missing_keys:
            missing_keys.sort()
            raise ConfigError('Config has missing keys: %s' % ', '.join(missing_keys))

        for key in required_keys:
            if not isinstance(data[key], dict):
                raise ConfigError('Config has illegal value for: %s' % key)

        contents = []
        for backup_path in data['contents']:
            source_path = data['contents'][backup_path]

            if not isinstance(source_path, str) and (source_path is not None):
                raise ConfigError(f'Illegal value for contents/{backup_path}: {source_path}')

            contents.append(Content(backup_path, source_path))

        return Config(
            contents,
            Destination.from_dict(data['destination'])
        )

    @staticmethod
    def from_file(path):
        """
        Create Config object from a YAML file.

        :except ConfigError

        :param path: path/to/config.yml
        :return: A Config object.
        """
        Logger.debug(f'Loading configuration: {path}')
        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError(error) from error

        return Config.from_dict(data)

    @staticmethod
    def locate(path: str) -> Optional[str]:
        """
        Looks up a config file and returns its absolute path.

        If a matching config file is not found, None is returned.

        :param path: some/config.yml.
        :return: /path/to/some/config.yml if found.
        """
        path = os.path.expanduser(path)
        message = 'Config not found at %s'

        if os.path.isabs(path):
            if os.path.isfile(path):
                return path

            Logger.debug(message % path)
            return None

        relative_path = os.path.join(os.getcwd(), path)
        if os.path.isfile(relative_path):
            return relative_path

        Logger.debug(message % relative_path)

        home_path = os.path.expanduser(f'~/{path}')
        if os.path.isfile(home_path):
            return home_path

        Logger.debug(message % home_path)

        return None

    @staticmethod
    def absolute_path(path: str) -> str:
        """
        Converts a config path to an absolute path.

        Example
        ------
        Input: ~/.clibato.yml
        Output: $HOME/.clibato.yml

        Example:
        ------
        Input: .clibato.yml
        Output: $CWD/.clibato.yml

        :param path: Config path.
        :return: Absolute path to config file.
        """
        path = os.path.expanduser(path)

        if os.path.isabs(path):
            return path

        return os.path.join(os.getcwd(), path)

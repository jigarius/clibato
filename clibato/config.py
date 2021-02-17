"""Clibato Configuration"""

import logging
from pathlib import Path
from typing import List, Optional
import yaml

from .error import ConfigError
from .content import Content
from .destination import Destination

logger = logging.getLogger('clibato')


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

        return Config(
            Content.from_dict(data['contents']),
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
        logger.info('Loading configuration: %s', path)
        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError(error) from error

        return Config.from_dict(data)

    @staticmethod
    def locate(path: Path) -> Optional[Path]:
        """
        Looks up a config file and returns its absolute path.

        If a matching config file is not found, None is returned.

        :param path: some/config.yml.
        :return: /path/to/some/config.yml if found.
        """
        path = path.expanduser()
        message = 'Config not found at %s'

        if path.is_absolute():
            if path.is_file():
                return path
            logger.debug(message, path)
            return None

        relative_path = path.resolve()
        if relative_path.is_file():
            return relative_path
        logger.debug(message, relative_path)

        home_path = Path.home() / path
        if home_path.is_file():
            return home_path
        logger.debug(message, home_path)

        return None

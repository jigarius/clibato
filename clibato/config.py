"""Clibato Configuration"""

from typing import List
import yaml

from . import utils
from .error import ConfigError
from .content import Content
from .destination import Destination


class Config:
    """Clibato Configuration"""

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

        :except KeyError
        """
        try:
            utils.ensure_shape(
                data,
                {'contents': {}, 'destination': {}}
            )
        except KeyError as error:
            raise ConfigError(error) from error

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
        """Create Config object from a YAML file."""
        path = utils.normalize_path(path)

        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError(error) from error

        return Config.from_dict(data)

"""Clibato Configuration"""

from typing import List
import yaml

from . import utils
from .error import ConfigError
from .content import Content
from .destination import Destination


class Config(utils.ConfigDict):
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
        path = utils.normalize_path(path)

        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                raise ConfigError(error) from error

        return Config(data)

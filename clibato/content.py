import os

from .error import ConfigError
from . import utils


class Content:
    """Clibato Content: An item for backup/restore."""
    def __init__(self, backup_path: str, config: dict = None):
        config = config or {}
        self._config = {
            **config,
            'backup': backup_path
        }

        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.source_path() == other.source_path() and
            self.backup_path() == other.backup_path()
        )

    def source_path(self) -> str:
        """Path to source file."""
        return self._config['source']

    def backup_path(self, prefix: str = '') -> str:
        """Path to backup file."""
        if prefix and not prefix.endswith('/'):
            prefix += '/'

        return f"{prefix}{self._config['backup']}"

    def _validate(self):
        if os.path.isabs(self._config['backup']):
            raise ConfigError('Backup path cannot be absolute')

        backup_path_parts = self._config['backup'].split('/')

        for illegal_part in ['.', '..', '~']:
            if illegal_part in backup_path_parts:
                raise ConfigError(f'Backup path cannot contain: {illegal_part}')

        if not self._config.get('source'):
            self._config['source'] = f'~/{self.backup_path()}'

        self._config['source'] = utils.normalize_path(self._config['source'])

        if not os.path.isabs(self._config['source']):
            raise ConfigError(f"Source path invalid: {self._config['source']}")

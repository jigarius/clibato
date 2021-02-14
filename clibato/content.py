import os

from .error import ConfigError


class Content:
    """Clibato Content: An item for backup/restore."""

    def __init__(self, backup_path: str, source_path: str = None):
        self._backup_path = backup_path
        self._source_path = source_path or f'~/{self._backup_path}'

        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.source_path() == other.source_path() and
            self.backup_path() == other.backup_path()
        )

    def source_path(self) -> str:
        """Path to source file."""
        return self._source_path

    def backup_path(self, prefix: str = '') -> str:
        """Path to backup file."""
        if prefix and not prefix.endswith('/'):
            prefix += '/'

        return f"{prefix}{self._backup_path}"

    def _validate(self):
        if os.path.isabs(self._backup_path):
            raise ConfigError(f'Backup path cannot be absolute: {self._backup_path}')

        backup_path_parts = self._backup_path.split('/')

        for illegal_part in ['.', '..', '~']:
            if illegal_part in backup_path_parts:
                raise ConfigError(f'Backup path cannot contain: {illegal_part}')

        self._source_path = os.path.expanduser(self._source_path)

        if not os.path.isabs(self._source_path):
            raise ConfigError(f"Source path invalid: {self._source_path}")

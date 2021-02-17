from pathlib import Path
from .error import ConfigError


class Content:
    """Clibato Content: An item for backup/restore."""

    def __init__(self, backup_path: str, source_path: str = None):
        self._backup_path = Path(backup_path)

        if source_path:
            self._source_path = Path(source_path)
        else:
            self._source_path = Path.home() / self._backup_path

        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.source_path() == other.source_path() and
            self.backup_path() == other.backup_path()
        )

    def source_path(self) -> Path:
        """Path to source file."""
        return self._source_path

    def backup_path(self) -> Path:
        """Path to backup file."""
        return self._backup_path

    def _validate(self):
        if self._backup_path.is_absolute():
            raise ConfigError(f'Backup path cannot be absolute: {self._backup_path}')

        for illegal_part in ['..', '~']:
            if illegal_part in self._backup_path.parts:
                raise ConfigError(f'Backup path cannot contain: {illegal_part}')

        self._source_path = self._source_path.expanduser()
        if not self._source_path.is_absolute():
            raise ConfigError(f"Source path invalid: {self._source_path}")

    @staticmethod
    def from_dict(data: dict):
        """
        Create Content objects from a dictionary.

        The keys of the dictionary should be the backup paths, and the values,
        if any, will be treated as source paths.

        :param data: A dictionary.
        :return: A list of Content objects.
        """
        contents = []
        for backup_path in data:
            source_path = data[backup_path]
            if not isinstance(source_path, str) and (source_path is not None):
                raise ConfigError(f'Illegal source path for {backup_path}: {source_path}')
            contents.append(Content(backup_path, source_path))

        return contents

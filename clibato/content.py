import os
import clibato


class Content:
    """Clibato Content: An item for backup/restore."""
    def __init__(self, backup_path: str, config: dict = None):
        config = config or {}
        self._config = {
            'source': '~/' + backup_path,
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
        return self._config.get('source')

    def backup_path(self) -> str:
        """Path to backup file."""
        return self._config.get('backup', None)

    def _validate(self):
        if not self.source_path():
            raise clibato.ConfigError('Invalid source path')

        if os.path.isabs(self.backup_path()):
            raise clibato.ConfigError('Backup path cannot be absolute')

        backup_path_parts = self.backup_path().split('/')

        for illegal_part in ['.', '..', '~']:
            if illegal_part in backup_path_parts:
                raise clibato.ConfigError(f'Backup path cannot contain: {illegal_part}')

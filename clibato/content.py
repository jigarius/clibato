import clibato


class Content:
    def __init__(self, backup_path: str, config: dict = {}):
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
        return self._config.get('source')

    def backup_path(self) -> str:
        return self._config.get('backup', None)

    def _validate(self):
        if not self.source_path():
            raise clibato.ConfigError('Invalid source path')

        backup_path_parts = self.backup_path().split('/')

        if backup_path_parts[0] == '':
            raise clibato.ConfigError('Backup path must not begin with /')

        for illegal_part in ['.', '..', '~']:
            if illegal_part in backup_path_parts:
                raise clibato.ConfigError(f'Backup path contains illegal part: {illegal_part}')

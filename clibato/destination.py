from shutil import copyfile
import os
import clibato


class Destination:
    """Clibato Backup Destination"""
    # TODO: Extend ConfigAbstract
    #   See https://docs.python.org/2/library/abc.html

    _DEFAULTS = {}

    def __init__(self, data: dict):
        if type(self) is Destination:
            raise NotImplementedError(f'Class not instantiable: {type(self).__name__}')

        if not data.get('type'):
            raise clibato.ConfigError('Key cannot be empty: type')

        self._data = clibato.Config.merge(self._DEFAULTS, data)
        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.data() == other.data()
        )

    def data(self):
        """Get the underlying configuration as a dictionary"""
        return {**self._data}

    def type(self) -> str:
        """Destination type"""
        return self._data['type']

    def backup(self, contents):
        """Backup the contents"""
        raise NotImplementedError()

    def restore(self, contents):
        """Restore the contents"""
        raise NotImplementedError()

    def _validate(self):
        pass

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Destination object from a dictionary.

        data.type determines the type of object.
        """
        tipo = data.get('type', None)

        if tipo == 'repository':
            return Repository(data)

        if tipo == 'directory':
            return Directory(data)

        raise clibato.ConfigError(f"Illegal type: {tipo}")


class Directory(Destination):
    """Destination type: Directory"""

    def backup(self, contents):
        for k in contents:
            content = contents[k]
            try:
                copyfile(
                    content.source_path(),
                    content.backup_path(self._path())
                )
                print(f'Backed up: {content.source_path()}')
            except FileNotFoundError:
                print(f'Source not found: {content.source_path()}')

    def restore(self, contents):
        for k in contents:
            content = contents[k]
            try:
                copyfile(
                    content.backup_path(self._path()),
                    content.source_path()
                )
                print(f'Restored: {content.source_path()}')
            except FileNotFoundError:
                print(f'Backup not found: {content.backup_path()}')

    def _path(self):
        return self._data['path']

    def _validate(self):
        if not self._data['path']:
            raise clibato.ConfigError('Key cannot be empty: path')

        if not os.path.isabs(self._data['path']):
            raise clibato.ConfigError(f'Path is not absolute: {self._path()}')

        if not os.path.isdir(self._path()):
            raise clibato.ConfigError(f'Path is not a directory: {self._path()}')


class Repository(Directory):
    """Destination type: Git Repository"""

    _DEFAULTS = {
        'path': None,
        'branch': 'main',
        'user': {
            'name': 'Clibato',
            'mail': 'clibato@jigarius.com'
        }
    }

    def backup(self, contents):
        pass

    def restore(self, contents):
        pass

    def _branch(self):
        return self._data.get('branch', None)

    def _user_name(self):
        return self._data['user']['name']

    def _user_mail(self):
        return self._data['user']['mail']

    def _validate(self):
        if not self._data['path']:
            raise clibato.ConfigError('Key cannot be empty: path')

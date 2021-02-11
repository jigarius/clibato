import os
import clibato


class Destination:
    # TODO: https://docs.python.org/2/library/abc.html

    """Clibato Backup Destination"""
    def __init__(self, data: dict):
        self._data = {**data}

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

    def restore(self, contents):
        """Restore the contents"""

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Destination object from a dictionary.

        data.type determines the type of object.
        """
        tipo = data.get('type', None)

        if tipo == 'repository':
            return Repository(data)

        raise clibato.ConfigError(f"Illegal type: {tipo}")


class Directory(Destination):
    """Destination type: Directory"""

    def __init__(self, data: dict):
        super().__init__(data)

        self._validate()

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

    _DEFAULT = {
        'path': None,
        'branch': 'main',
        'user': {
            'name': 'Clibato',
            'mail': 'clibato@jigarius.com'
        }
    }

    def __init__(self, data: dict):
        data = clibato.Config.merge(self._DEFAULT, data)
        super().__init__(data)

        self._validate()

    def _branch(self):
        return self._data.get('branch', None)

    def _user_name(self):
        return self._data['user']['name']

    def _user_mail(self):
        return self._data['user']['mail']

    def _validate(self):
        if not self._data['path']:
            raise clibato.ConfigError('Key cannot be empty: path')
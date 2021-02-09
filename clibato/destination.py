import clibato


class Destination:
    """Clibato Backup Destination"""
    def __init__(self, data: dict):
        self._data = {**data}

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.__dict__ == other.__dict__
        )

    def type(self) -> str:
        """Destination type"""
        return self._data['type']

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


class Repository(Destination):
    """Destination type: Git Repository"""
    _DEFAULT_USER_NAME = 'Clibato'
    _DEFAULT_USER_MAIL = 'clibato@jigarius.com'
    _DEFAULT_BRANCH = 'main'

    def __init__(self, data: dict):
        super().__init__(data)

        self._validate()

    def _remote(self):
        return self._data.get('remote', None)

    def _branch(self):
        return self._data.get('branch', None) or self._DEFAULT_BRANCH

    def _user_name(self):
        return clibato.Config.extract(self._data, 'user.name') or self._DEFAULT_USER_NAME

    def _user_mail(self):
        return clibato.Config.extract(self._data, 'user.mail') or self._DEFAULT_USER_MAIL

    def _validate(self):
        if not self._remote():
            raise clibato.ConfigError('Key cannot be empty: remote')

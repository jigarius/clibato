import typing
import clibato


class Destination:
    def __init__(self, data: dict):
        self._data = {**data}

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.__dict__ == other.__dict__
        )

    def type(self):
        return self._data['type']

    @staticmethod
    def from_dict(data: dict):
        type = data.get('type', None)

        if type == 'repository':
            return Repository(data)

        raise clibato.ConfigError(f"Illegal type: {type}")


class Repository(Destination):
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
        return Config.extract(self._data, 'user.name') or self._DEFAULT_USER_NAME

    def _user_mail(self):
        return Config.extract(self._data, 'user.mail') or self._DEFAULT_USER_MAIL

    def _validate(self):
        if not self._remote():
            raise ConfigError('Key cannot be empty: remote')

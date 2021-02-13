from shutil import copyfile
import os
from git import Repo, Actor

from . import utils
from .error import ConfigError
from .logger import Logger


class Destination(utils.ConfigDict):
    """Clibato Backup Destination"""

    def __init__(self, data: dict):
        if type(self) is Destination:
            raise NotImplementedError(f'Class not instantiable: {type(self).__name__}')

        super().__init__(data)

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.data() == other.data()
        )

    def data(self):
        """Get the underlying configuration as a dictionary"""
        return {**self._data}

    def backup(self, contents):
        """Backup the contents"""
        raise NotImplementedError()

    def restore(self, contents):
        """Restore the contents"""
        raise NotImplementedError()

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Destination object from a dictionary.

        data.type determines the type of object.
        """
        tipo = data.pop('type', None)

        if tipo == 'repository':
            return Repository(data)

        if tipo == 'directory':
            return Directory(data)

        raise ConfigError(f"Illegal type: {tipo}")


class Directory(Destination):
    """Destination type: Directory"""

    _DEFAULTS = {
        'path': None
    }

    def backup(self, contents):
        for k in contents:
            content = contents[k]
            try:
                copyfile(
                    content.source_path(),
                    content.backup_path(self._path())
                )
                Logger.info(f'Backed up: {content.source_path()}')
            except FileNotFoundError:
                Logger.error(f'Source not found: {content.source_path()}')

    def restore(self, contents):
        for k in contents:
            content = contents[k]
            try:
                copyfile(
                    content.backup_path(self._path()),
                    content.source_path()
                )
                Logger.info(f'Restored: {content.source_path()}')
            except FileNotFoundError:
                Logger.error(f'Backup not found: {content.backup_path()}')

    def _path(self):
        return self._data['path']

    def _validate(self):
        super()._validate()

        if not self._data['path']:
            raise ConfigError('Key cannot be empty: path')

        self._data['path'] = utils.normalize_path(self._data['path'])

        if not os.path.isabs(self._data['path']):
            raise ConfigError(f'Path is not absolute: {self._path()}')

        if not os.path.isdir(self._path()):
            raise ConfigError(f'Path is not a directory: {self._path()}')


class Repository(Directory):
    """Destination type: Git Repository"""

    _DEFAULTS = {
        'path': None,
        'remote': None,
        'branch': 'main',
        'user': {
            'name': 'Clibato',
            'mail': 'clibato@jigarius.com'
        }
    }

    def __init__(self, data: dict):
        super().__init__(data)
        self._repo = None

    def backup(self, contents):
        self._git_init()
        self._git_pull()

        repo = self._repo

        if repo.is_dirty():
            Logger.error(f'Uncommitted changes found in: {self._path()}')
            Logger.info('Commit or discard all changes and try again.')
            return

        super().backup(contents)

        index = repo.index
        index.reset()
        for k in contents:
            index.add(contents[k].backup_path())

        change_count = len(repo.index.diff(None))
        Logger.info(f'{change_count} change(s) detected.')

        if change_count == 0:
            return

        self._git_commit('Clibato backup')
        self._git_push()

    def restore(self, contents):
        self._git_init()
        self._git_pull()

        super().restore(contents)

    def _remote(self):
        return self._data['remote']

    def _branch(self):
        return self._data['branch']

    def _validate(self):
        super()._validate()

        if not self._data['remote']:
            raise ConfigError('Key cannot be empty: remote')

    def _git_commit(self, message):
        author = Actor(self._data['user']['name'], self._data['user']['mail'])
        self._repo.index.commit(message, author=author)

    def _git_init(self):
        """Prepare Git repo and remote."""
        if self._repo:
            return

        self._repo = repo = Repo.init(self._path(), mkdir=False)

        if 'origin' in repo.remotes:
            if repo.remotes.origin.url != self._remote():
                Logger.debug(f'Removing incorrect remote: {repo.remotes.origin.url}')
                repo.delete_remote(repo.remotes.origin)

        if 'origin' not in repo.remotes:
            Logger.info(f'Adding remote: {self._remote()} (origin)')
            repo.create_remote('origin', self._remote())

    def _git_pull(self):
        """Switch branch and pull remote changes."""
        repo = self._repo
        remote = repo.remotes.origin
        remote.fetch()

        if self._branch() not in repo.branches:
            Logger.info(f'Creating branch: {self._branch()}')
            self._git_commit('Initial commit')
            repo.create_head(self._branch())

        if repo.active_branch != self._branch():
            Logger.info(f'Switching branch: {self._branch()}')
            repo.heads[self._branch()].checkout()

    def _git_push(self):
        """Push commits to remote."""
        Logger.info(f'Pushing commits to origin {self._branch()}.')
        self._repo.remotes.origin.push(self._branch())

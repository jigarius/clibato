from shutil import copyfile
import os
from git import Repo, Actor

from .error import ConfigError
from .logger import Logger


class Destination:
    """Clibato Backup Destination"""

    def __init__(self):
        if type(self) is Destination:
            raise NotImplementedError(f'Class not instantiable: {type(self).__name__}')

    def __eq__(self, other):
        raise NotImplementedError()

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
        try:
            tipo = data.pop('type', None)

            if tipo == 'repository':
                return Repository(**data)
            if tipo == 'directory':
                return Directory(**data)

            raise ConfigError(f"Illegal type: {tipo}")
        except TypeError as error:
            raise ConfigError(error) from error


class Directory(Destination):
    """Destination type: Directory"""

    def __init__(self, path):
        super().__init__()

        self._path = path
        self._validate()

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self._path == other._path
        )

    def path(self):
        """Storage path"""
        return self._path

    def backup(self, contents):
        for content in contents:
            try:
                backup_path = content.backup_path(self._path)

                # Ensure backup directory exists.
                backup_dir = os.path.dirname(backup_path)
                if not os.path.isdir(backup_dir):
                    Logger.debug(f'Created directory: {backup_dir}')
                    os.makedirs(backup_dir)

                copyfile(
                    content.source_path(),
                    backup_path
                )

                Logger.info(f'Backed up: {content.source_path()}')
            except FileNotFoundError as error:
                Logger.error(error)

    def restore(self, contents):
        for content in contents:
            try:
                copyfile(
                    content.backup_path(self._path),
                    content.source_path()
                )
                Logger.info(f'Restored: {content.source_path()}')
            except FileNotFoundError:
                Logger.error(f'Backup not found: {content.backup_path()}')

    def _validate(self):
        if not self._path:
            raise ConfigError('Path cannot be empty')

        self._path = os.path.expanduser(self._path)

        if not os.path.isabs(self._path):
            raise ConfigError(f'Path is not absolute: {self._path}')

        if not os.path.isdir(self._path):
            raise ConfigError(f'Path is not a directory: {self._path}')


class Repository(Directory):
    """Destination type: Git Repository"""

    def __init__(self, path, remote, branch=None, user_name=None, user_mail=None):
        self._repo = None
        self._author = Actor(
            user_name or 'Clibato',
            user_mail or 'clibato@jigarius.com'
        )
        self._remote = remote
        self._branch = branch or 'main'

        super().__init__(path)

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self._path == other._path and
            self._remote == other._remote and
            self._branch == other._branch and
            self._author == other._author
        )

    def backup(self, contents):
        self._git_init()
        self._git_pull()

        repo = self._repo

        if repo.is_dirty():
            Logger.error(f'Uncommitted changes found in: {self._path}')
            Logger.info('Commit or discard all changes and try again.')
            return

        super().backup(contents)

        index = repo.index
        index.reset()
        for content in contents:
            index.add(content.backup_path())

        change_count = len(repo.index.diff('HEAD'))
        Logger.info(f'{change_count} change(s) detected.')

        if change_count == 0:
            return

        self._git_commit('Clibato backup')
        self._git_push()

    def restore(self, contents):
        self._git_init()
        self._git_pull()

        super().restore(contents)

    def _validate(self):
        super()._validate()

        if not self._remote:
            raise ConfigError('Remote cannot be empty')

    def _git_commit(self, message):
        self._repo.index.commit(message, author=self._author)

    def _git_init(self):
        """Prepare Git repo and remote."""
        if self._repo:
            return

        self._repo = repo = Repo.init(self._path, mkdir=False)

        if 'origin' in repo.remotes:
            if repo.remotes.origin.url != self._remote:
                Logger.debug(f'Removing incorrect remote: {repo.remotes.origin.url}')
                repo.delete_remote(repo.remotes.origin)

        if 'origin' not in repo.remotes:
            Logger.info(f'Adding remote: {self._remote} (origin)')
            repo.create_remote('origin', self._remote)

    def _git_pull(self):
        """Switch branch and pull remote changes."""
        repo = self._repo
        remote = repo.remotes.origin
        remote.fetch()

        if self._branch not in repo.branches:
            Logger.info(f'Creating branch: {self._branch}')
            self._git_commit('Initial commit')
            repo.create_head(self._branch)

        if repo.active_branch != self._branch:
            Logger.info(f'Switching branch: {self._branch}')
            repo.heads[self._branch].checkout()

    def _git_push(self):
        """Push commits to remote."""
        Logger.info(f'Pushing commits to origin {self._branch}.')
        self._repo.remotes.origin.push(self._branch)

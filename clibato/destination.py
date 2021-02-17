from shutil import copyfile
from pathlib import Path
import logging
import os
from git import Repo, Actor

from .error import ActionError, ConfigError

logger = logging.getLogger('clibato')


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

    @staticmethod
    def _ensure_directory(path: Path) -> None:
        """
        Creates the directory if it doesn't exist

        :param path: Directory path.
        :return: None
        """
        if path.is_dir():
            return

        logger.debug('Creating directory: %s', path)
        os.makedirs(path)


class Directory(Destination):
    """Destination type: Directory"""

    def __init__(self, path: str):
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
                backup_path = self._path / content.backup_path()
                Destination._ensure_directory(backup_path.parent)
                copyfile(content.source_path(), backup_path)
                logger.info('Backed up: %s', content.source_path())
            except FileNotFoundError as error:
                logger.error(error)

    def restore(self, contents):
        for content in contents:
            try:
                Destination._ensure_directory(content.source_path().parent)
                copyfile(self._path / content.backup_path(), content.source_path())
                logger.info('Restored: %s', content.source_path())
            except FileNotFoundError as error:
                logger.error(error)

    def _validate(self):
        if not self._path:
            raise ConfigError('Path cannot be empty')

        self._path = Path(self._path).expanduser()

        if not self._path.is_absolute():
            raise ConfigError(f'Path is not absolute: {self._path}')

        if not self._path.is_dir():
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
            raise ActionError(
                f'Uncommitted changes found in: {self._path}.'
                'Commit or discard all changes and try again.'
            )

        super().backup(contents)

        index = repo.index
        index.reset()
        for content in contents:
            index.add(str(content.backup_path()))

        change_count = len(repo.index.diff('HEAD'))
        logger.info('%d change(s) detected.', change_count)

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
                logger.info('Removing incorrect remote: %s', repo.remotes.origin.url)
                repo.delete_remote(repo.remotes.origin)

        if 'origin' not in repo.remotes:
            logger.info('Creating remote: %s (origin)', self._remote)
            repo.create_remote('origin', self._remote)

    def _git_pull(self):
        """Switch branch and pull remote changes."""
        repo = self._repo
        remote = repo.remotes.origin
        remote.fetch()

        if self._branch not in repo.branches:
            logger.info('Creating branch: %s', self._branch)
            self._git_commit('Initial commit')
            repo.create_head(self._branch)

        if repo.active_branch != self._branch:
            logger.info('Switching branch: %s', self._branch)
            repo.heads[self._branch].checkout()

    def _git_push(self):
        """Push commits to remote."""
        logger.info('Pushing commits to origin/%s.', self._branch)
        self._repo.remotes.origin.push(self._branch)

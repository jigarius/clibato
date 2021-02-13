import os
import unittest

from clibato import Content, ConfigError


class TestContent(unittest.TestCase):
    _HOME_PATH = os.path.expanduser('~')

    def test__eq__(self):
        subject = Content('todo.txt', '/var/todo.txt')

        self.assertEqual(
            subject,
            Content('todo.txt', '/var/todo.txt')
        )

        self.assertNotEqual(
            subject,
            Content('done.txt', '/var/www/todo.txt')
        )

        self.assertNotEqual(
            subject,
            Content('todo.txt', '/var/www/todo.txt')
        )

    def test_backup_path(self):
        content = Content('.bashrc')
        self.assertEqual(content.backup_path(), '.bashrc')

    def test_backup_path_with_prefix(self):
        content = Content('.bashrc')
        self.assertEqual(
            content.backup_path('/backup'),
            '/backup/.bashrc'
        )

    def test_source_path(self):
        content = Content('todo.txt', '/users/jigarius/todo.txt')

        self.assertEqual(
            content.source_path(),
            f'/users/jigarius/todo.txt'
        )

    def test_source_path_with_tilde(self):
        content = Content('todo.txt', '~/Documents/todo.txt')

        self.assertEqual(
            content.source_path(),
            f'{self._HOME_PATH}/Documents/todo.txt'
        )

    def test_source_path_cannot_be_relative(self):
        with self.assertRaises(ConfigError) as context:
            Content('todo.txt', 'Documents/todo.txt')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Source path invalid: Documents/todo.txt'
        )

    def test_source_path_when_empty(self):
        content = Content('todo.txt', '')

        self.assertEqual(
            content.source_path(),
            f'{self._HOME_PATH}/todo.txt'
        )

    def test_source_path_when_undefined(self):
        content = Content('.bashrc')

        self.assertEqual(
            content.source_path(),
            f'{self._HOME_PATH}/.bashrc'
        )

    def test_backup_path_cannot_be_absolute(self):
        with self.assertRaises(ConfigError) as context:
            Content('/.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot be absolute'
        )

    def test_backup_path_cannot_have_tilde(self):
        with self.assertRaises(ConfigError) as context:
            Content('~/.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: ~'
        )

    def test_backup_path_cannot_have_single_dot(self):
        with self.assertRaises(ConfigError) as context:
            Content('./.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: .'
        )

    def test_backup_path_cannot_have_double_dot(self):
        with self.assertRaises(ConfigError) as context:
            Content('../.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: ..'
        )

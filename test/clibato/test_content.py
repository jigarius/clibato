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
        subject = Content('.bashrc')

        self.assertEqual(
            '.bashrc',
            subject.backup_path()
        )

    def test_backup_path_with_prefix(self):
        subject = Content('.bashrc')

        self.assertEqual(
            '/backup/.bashrc',
            subject.backup_path('/backup')
        )

    def test_source_path(self):
        subject = Content('todo.txt', '/users/jigarius/todo.txt')

        self.assertEqual(
            f'/users/jigarius/todo.txt',
            subject.source_path()
        )

    def test_source_path_with_tilde(self):
        subject = Content('todo.txt', '~/Documents/todo.txt')

        self.assertEqual(
            os.path.join(self._HOME_PATH, 'Documents', 'todo.txt'),
            subject.source_path()
        )

    def test_source_path_cannot_be_relative(self):
        with self.assertRaises(ConfigError) as context:
            Content('todo.txt', 'Documents/todo.txt')

        self.assertEqual(
            'Source path invalid: Documents/todo.txt',
            str(context.exception).strip("'")
        )

    def test_source_path_when_empty(self):
        subject = Content('todo.txt', '')

        self.assertEqual(
            os.path.join(self._HOME_PATH, 'todo.txt'),
            subject.source_path()
        )

    def test_source_path_when_undefined(self):
        subject = Content('.bashrc')

        self.assertEqual(
            os.path.join(self._HOME_PATH, '.bashrc'),
            subject.source_path()
        )

    def test_backup_path_cannot_be_absolute(self):
        with self.assertRaises(ConfigError) as context:
            Content('/.bashrc')

        self.assertEqual(
            'Backup path cannot be absolute: /.bashrc',
            str(context.exception).strip("'")
        )

    def test_backup_path_cannot_have_tilde(self):
        with self.assertRaises(ConfigError) as context:
            Content('~/.bashrc')

        self.assertEqual(
            'Backup path cannot contain: ~',
            str(context.exception).strip("'")
        )

    def test_backup_path_cannot_have_single_dot(self):
        with self.assertRaises(ConfigError) as context:
            Content('./.bashrc')

        self.assertEqual(
            'Backup path cannot contain: .',
            str(context.exception).strip("'")
        )

    def test_backup_path_cannot_have_double_dot(self):
        with self.assertRaises(ConfigError) as context:
            Content('../.bashrc')

        self.assertEqual(
            'Backup path cannot contain: ..',
            str(context.exception).strip("'")
        )

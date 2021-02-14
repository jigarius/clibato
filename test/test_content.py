import os
import unittest

from clibato import Content, ConfigError


class TestContent(unittest.TestCase):
    """Test clibato.Content"""

    _HOME_PATH = os.path.expanduser('~')

    def test__eq__(self):
        """.__eq__()"""
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
        """.backup_path() works"""
        subject = Content('.bashrc')

        self.assertEqual(
            '.bashrc',
            subject.backup_path()
        )

    def test_backup_path_with_prefix(self):
        """.backup_path() works with a prefix"""
        subject = Content('.bashrc')

        self.assertEqual(
            '/backup/.bashrc',
            subject.backup_path('/backup')
        )

    def test_source_path(self):
        """.new() works with absolute source paths"""
        subject = Content('todo.txt', '/users/jigarius/todo.txt')

        self.assertEqual(
            '/users/jigarius/todo.txt',
            subject.source_path()
        )

    def test_source_path_with_tilde(self):
        """.new() works with source paths starting with tilde"""
        subject = Content('todo.txt', '~/Documents/todo.txt')

        self.assertEqual(
            os.path.join(self._HOME_PATH, 'Documents', 'todo.txt'),
            subject.source_path()
        )

    def test_source_path_cannot_be_relative(self):
        """.new() raises if source_path is relative"""
        message = 'Source path invalid: Documents/todo.txt'
        with self.assertRaisesRegex(ConfigError, message):
            Content('todo.txt', 'Documents/todo.txt')

    def test_source_path_when_empty(self):
        """.new() works when source_path is empty"""
        subject = Content('todo.txt', '')

        self.assertEqual(
            os.path.join(self._HOME_PATH, 'todo.txt'),
            subject.source_path()
        )

    def test_source_path_when_undefined(self):
        """.new() works when source_path is None"""
        subject = Content('.bashrc')

        self.assertEqual(
            os.path.join(self._HOME_PATH, '.bashrc'),
            subject.source_path()
        )

    def test_backup_path_cannot_be_absolute(self):
        """.new() raises if backup path is not absolute"""
        message = 'Backup path cannot be absolute: /.bashrc'
        with self.assertRaisesRegex(ConfigError, message):
            Content('/.bashrc')

    def test_backup_path_cannot_contain_illegal_elements(self):
        """.new() raises if backup path contains illegal elements"""
        illegal_parts = ['~', '.', '..']

        for part in illegal_parts:
            message = f'Backup path cannot contain: {part}'
            with self.assertRaisesRegex(ConfigError, message):
                Content(f'{part}/.bashrc')

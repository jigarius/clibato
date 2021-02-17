import unittest
from pathlib import Path
from clibato import Content, ConfigError


class TestContent(unittest.TestCase):
    """Test clibato.Content"""

    def test__eq__(self):
        """.__eq__()"""
        source_path = str(Path('~', 'todo.txt'))
        subject = Content('todo.txt', source_path)

        self.assertEqual(
            subject,
            Content('todo.txt', source_path)
        )

        self.assertNotEqual(
            subject,
            Content('done.txt', str(Path('~', 'done.txt')))
        )

    def test_from_dict(self):
        """.from_dict()"""
        self.assertEqual(
            [Content('.bashrc', None)],
            Content.from_dict({'.bashrc': None})
        )

    def test_from_dict_source_path_cannot_be_dictionary(self):
        """.from_dict() fails if content entry is a dictionary"""
        with self.assertRaisesRegex(ConfigError, 'Illegal source path for .bashrc: {}'):
            Content.from_dict({'.bashrc': {}})

    def test_backup_path(self):
        """.backup_path() works"""
        subject = Content('.bashrc')

        self.assertEqual(Path('.bashrc'), subject.backup_path())

    def test_source_path_with_absolute_path(self):
        """.new() works with absolute source paths"""
        source_path = Path('/', 'todo.txt')
        subject = Content('todo.txt', str(source_path))

        self.assertEqual(source_path, subject.source_path())

    def test_source_path_with_tilde(self):
        """.new() works with source paths starting with tilde"""
        source_path = Path('~', 'Documents', 'todo.txt')
        subject = Content('todo.txt', str(source_path))

        self.assertEqual(
            source_path.expanduser().absolute(),
            subject.source_path()
        )

    def test_source_path_with_relative_path(self):
        """.new() raises if source_path is relative"""
        message = 'Source path invalid: Documents/todo.txt'
        with self.assertRaisesRegex(ConfigError, message):
            Content('todo.txt', 'Documents/todo.txt')

    def test_source_path_when_empty(self):
        """.new() works when source_path is empty"""
        subject = Content('.bashrc', '')

        self.assertEqual(
            Path('~', '.bashrc').expanduser(),
            subject.source_path()
        )

    def test_source_path_when_undefined(self):
        """.new() works when source_path is None"""
        subject = Content('.bashrc')

        self.assertEqual(
            Path('~', '.bashrc').expanduser(),
            subject.source_path()
        )

    def test_backup_path_cannot_be_absolute(self):
        """.new() raises if backup path is not absolute"""
        message = 'Backup path cannot be absolute: /.bashrc'
        with self.assertRaisesRegex(ConfigError, message):
            Content(str(Path('/', '.bashrc')))

    def test_backup_path_cannot_contain_illegal_elements(self):
        """.new() raises if backup path contains illegal elements"""
        illegal_parts = ['~', '..']

        for part in illegal_parts:
            message = f'Backup path cannot contain: {part}'
            with self.assertRaisesRegex(ConfigError, message):
                Content(str(Path(part, '.bashrc')))

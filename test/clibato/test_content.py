import unittest
import clibato


class TestContent(unittest.TestCase):
    def test_backup_path(self):
        content = clibato.Content('.bashrc')
        self.assertEqual(content.backup_path(), '.bashrc')

    def test_source_path(self):
        content = clibato.Content(
            'todo.txt',
            {'source': '~/Documents/todo.txt'}
        )
        self.assertEqual(content.source_path(), '~/Documents/todo.txt')

    def test_source_path_when_undefined(self):
        content = clibato.Content('.bashrc')
        self.assertEqual(content.source_path(), '~/.bashrc')

    def test_backup_path_cannot_be_absolute(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Content('/.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot be absolute'
        )

    def test_backup_path_cannot_have_tilde(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Content('~/.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: ~'
        )

    def test_backup_path_cannot_have_single_dot(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Content('./.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: .'
        )

    def test_backup_path_cannot_have_double_dot(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Content('../.bashrc')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Backup path cannot contain: ..'
        )

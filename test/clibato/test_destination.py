import unittest

from clibato import Content, ConfigError, destination, utils
from .support import FileSystem


class TestDestination(unittest.TestCase):
    def test_new_not_allowed(self):
        with self.assertRaises(NotImplementedError) as context:
            destination.Destination({'type': 'directory', 'path': '/tmp'})

        self.assertEqual(
            str(context.exception).strip("'"),
            f'Class not instantiable: {destination.Destination.__name__}'
        )

    def test_from_dict_with_valid_type(self):
        subject = destination.Destination.from_dict({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(
            subject,
            destination.Directory({'path': '/tmp'})
        )

    def test_from_dict_with_illegal_type(self):
        with self.assertRaises(ConfigError) as context:
            destination.Destination.from_dict({'type': 'foobar'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Illegal type: foobar'
        )

    def test__eq__(self):
        subject = destination.Directory({'path': '/tmp'})

        self.assertEqual(
            subject,
            destination.Directory({'path': '/tmp'})
        )

        self.assertNotEqual(
            subject,
            destination.Directory({'path': '/var/www'})
        )

        self.assertNotEqual(
            subject,
            destination.Repository({
                'path': '/tmp',
                'remote': 'git@github.com:bunny/wabbit.git'
            })
        )


class TestDirectory(unittest.TestCase):
    def setUp(self):
        FileSystem.ensure('~/backup')
        FileSystem.ensure('~/source')

    def tearDown(self):
        FileSystem.unlink('~/backup')
        FileSystem.unlink('~/source')

    def test_new(self):
        subject = destination.Directory({'path': '/tmp'})

        self.assertEqual(
            subject.data(),
            {'path': '/tmp'}
        )

    def test_inheritance(self):
        self.assertTrue(issubclass(
            destination.Directory,
            destination.Destination
        ))

    def test_path_is_required(self):
        with self.assertRaises(ConfigError) as context:
            destination.Directory({'path': ''})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: path'
        )

    def test_path_is_absolute(self):
        with self.assertRaises(ConfigError) as context:
            destination.Directory({'path': 'foo/bar'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not absolute: foo/bar'
        )

    def test_path_is_directory(self):
        with self.assertRaises(ConfigError) as context:
            destination.Directory({'path': '/tmp/foo'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not a directory: /tmp/foo'
        )

    def test_path_is_tilde(self):
        subject = destination.Directory({'path': '~/backup'})

        self.assertEqual(
            subject.data(),
            {
                'path': utils.normalize_path('~/backup')
            }
        )

    def test_backup(self):
        FileSystem.write_file('~/.bunny', 'I am a bunny')

        subject = destination.Directory({'path': '~/backup'})

        subject.backup([Content('.bunny')])

        self.assertEqual(
            FileSystem.read_file('~/backup/.bunny'),
            'I am a bunny'
        )

    @unittest.skip('TODO')
    def test_backup_file_not_found(self):
        pass

    def test_restore(self):
        FileSystem.write_file('~/backup/.bunny', 'I am a bunny')

        subject = destination.Directory({'path': '~/backup'})

        subject.restore([Content('.bunny')])

        self.assertEqual(
            FileSystem.read_file('~/.bunny'),
            'I am a bunny'
        )

    @unittest.skip('TODO')
    def test_restore_file_not_found(self):
        pass


class TestRepository(unittest.TestCase):
    def test_new(self):
        subject = destination.Repository({
            'path': '/tmp',
            'remote': 'git@github.com:jigarius/clibato.git',
            'branch': 'backup',
            'user': {
                'name': 'Jigarius',
                'mail': 'jigarius@example.com',
            }
        })

        self.assertEqual(
            subject.data(),
            {
                'path': '/tmp',
                'remote': 'git@github.com:jigarius/clibato.git',
                'branch': 'backup',
                'user': {
                    'name': 'Jigarius',
                    'mail': 'jigarius@example.com',
                }
            }
        )

    def test_inheritance(self):
        self.assertTrue(issubclass(
            destination.Repository,
            destination.Directory
        ))

    def test_path_is_required(self):
        with self.assertRaises(ConfigError) as context:
            destination.Repository({
                'remote': 'git@github.com:jigarius/clibato.git',
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: path'
        )

    def test_remote_is_required(self):
        with self.assertRaises(ConfigError) as context:
            destination.Repository({
                'path': '/tmp',
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            'Key cannot be empty: remote'
        )

    def test_default_values_merged(self):
        subject = destination.Repository({
            'path': '/tmp',
            'remote': 'git@github.com:jigarius/clibato.git'
        })

        self.assertEqual(
            subject.data(),
            {
                'path': '/tmp',
                'remote': 'git@github.com:jigarius/clibato.git',
                'branch': 'main',
                'user': {
                    'name': 'Clibato',
                    'mail': 'clibato@jigarius.com'
                }
            }
        )

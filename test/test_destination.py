import os
import unittest

from clibato import Content, ConfigError, Destination, Directory, Repository
from .support import FileSystem


class TestDestination(unittest.TestCase):
    """Test destination.Destination"""

    def test_new(self):
        """Destination cannot be instantiated."""
        message = f'Class not instantiable: {Destination.__name__}'
        with self.assertRaisesRegex(NotImplementedError, message):
            Destination()

    def test_from_dict(self):
        """.from_dict() works with a valid dict"""
        subject = Destination.from_dict({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(
            subject,
            Directory('/tmp')
        )

    def test_from_dict_with_illegal_type(self):
        """.from_dict() fails with an invalid dict"""
        message = 'Illegal type: foobar'
        with self.assertRaisesRegex(ConfigError, message):
            Destination.from_dict({'type': 'foobar'})

    def test_from_dict_with_arg_mismatch(self):
        """.from_dict() fails with on argument mismatch"""
        with self.assertRaises(ConfigError):
            Destination.from_dict({
                'type': 'directory',
                'remote': 'git@github.com:jigarius/clibato.git'
            })


class TestDirectory(unittest.TestCase):
    """Test destination.Directory"""

    def setUp(self):
        FileSystem.ensure('~/backup')

    def tearDown(self):
        FileSystem.remove('~/backup')

    def test_new(self):
        """Instance creation."""
        subject = Directory('/tmp')

        self.assertIsInstance(subject, Directory)

    def test__eq__(self):
        """__eq__()"""
        subject = Directory('/tmp')

        self.assertEqual(
            subject,
            Directory('/tmp')
        )

        self.assertNotEqual(
            subject,
            Directory('~/')
        )

        self.assertNotEqual(
            subject,
            Repository('/tmp', 'git@github.com:bunny/wabbit.git')
        )

    def test_inheritance(self):
        """Directory must extend Destination"""
        self.assertTrue(issubclass(
            Directory,
            Destination
        ))

    def test_path(self):
        """.path()"""
        subject = Directory('/tmp')

        self.assertEqual('/tmp', subject.path())

    def test_path_cannot_be_empty(self):
        """Path cannot be empty"""
        message = 'Path cannot be empty'
        with self.assertRaisesRegex(ConfigError, message):
            Directory('')

    def test_path_must_be_absolute(self):
        """Path must be absolute"""
        message = 'Path is not absolute: foo/bar'
        with self.assertRaisesRegex(ConfigError, message):
            Directory('foo/bar')

    def test_path_must_be_directory(self):
        """Path must be a directory"""
        message = 'Path is not a directory: /tmp/foo'
        with self.assertRaisesRegex(ConfigError, message):
            Directory('/tmp/foo')

    def test_path_has_tilde(self):
        """Path cannot contain tilde (~)"""
        subject = Directory('~/backup')

        self.assertEqual(
            os.path.expanduser('~/backup'),
            subject.path()
        )

    def test_backup(self):
        """.backup()"""
        FileSystem.ensure('~/hole')
        FileSystem.write_file('~/.bunny', 'I am a bunny')
        FileSystem.write_file('~/hole/.wabbit', 'I am a wabbit')

        subject = Directory('~/backup')
        subject.backup([
            Content('.bunny'),
            Content('hole/.wabbit')
        ])

        self.assertEqual(
            'I am a bunny',
            FileSystem.read_file('~/backup/.bunny')
        )
        self.assertEqual(
            'I am a wabbit',
            FileSystem.read_file('~/backup/hole/.wabbit')
        )

        FileSystem.remove('~/.bunny')
        FileSystem.remove('~/hole/.wabbit')

    @unittest.skip('TODO')
    def test_backup_file_not_found(self):
        """.backup() logs if a file is not found"""

    def test_restore(self):
        """.restore()"""
        FileSystem.write_file('~/backup/.bunny', 'I am a bunny')

        subject = Directory('~/backup')
        subject.restore([Content('.bunny')])

        self.assertEqual(
            'I am a bunny',
            FileSystem.read_file('~/.bunny')
        )

    @unittest.skip('TODO')
    def test_restore_file_not_found(self):
        """.restore() logs if a file is not found"""


class TestRepository(unittest.TestCase):
    """Test destination.Repository"""

    def test_new(self):
        """Instance creation."""
        subject = Repository(
            '/tmp',
            'git@github.com:jigarius/clibato.git',
            'backup',
            'Jigarius',
            'jigarius@example.com',
        )

        self.assertIsInstance(subject, Repository)

    def test__eq__(self):
        """__eq__()"""
        subject = Repository('/tmp', 'git@github.com:bunny/wabbit.git')

        self.assertEqual(
            subject,
            Repository('/tmp', 'git@github.com:bunny/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Repository('/tmp', 'git@github.com:bucky/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Directory('/tmp')
        )

    def test_inheritance(self):
        """Repository must extend Directory"""
        self.assertTrue(issubclass(Repository, Directory))

    def test_path_cannot_be_empty(self):
        """Path cannot be empty"""
        message = 'Path cannot be empty'
        with self.assertRaisesRegex(ConfigError, message):
            Repository('', 'git@github.com:jigarius/clibato.git')

    def test_remote_cannot_be_empty(self):
        """Remote cannot be empty"""
        message = 'Remote cannot be empty'
        with self.assertRaisesRegex(ConfigError, message):
            Repository('/tmp', '')

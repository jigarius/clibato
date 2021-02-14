import os
import unittest

from clibato import Content, ConfigError, utils
from clibato.destination import *
from .support import FileSystem


class TestDestination(unittest.TestCase):
    def test_new_not_allowed(self):
        with self.assertRaises(NotImplementedError) as context:
            Destination()

        self.assertEqual(
            str(context.exception).strip("'"),
            f'Class not instantiable: {Destination.__name__}'
        )

    def test_from_dict(self):
        subject = Destination.from_dict({
            'type': 'directory',
            'path': '/tmp'
        })

        self.assertEqual(
            subject,
            Directory('/tmp')
        )

    def test_from_dict_with_illegal_type(self):
        with self.assertRaises(ConfigError) as context:
            Destination.from_dict({'type': 'foobar'})

        self.assertEqual(
            str(context.exception).strip("'"),
            'Illegal type: foobar'
        )


class TestDirectory(unittest.TestCase):
    def setUp(self):
        FileSystem.ensure('~/backup')
        FileSystem.ensure('~/source')

    def tearDown(self):
        FileSystem.unlink('~/backup')
        FileSystem.unlink('~/source')

    def test_new(self):
        subject = Directory('/tmp')

        self.assertIsInstance(subject, Directory)

    def test__eq__(self):
        subject = Directory('/tmp')

        self.assertEqual(
            subject,
            Directory('/tmp')
        )

        self.assertNotEqual(
            subject,
            Directory('/var/www')
        )

        self.assertNotEqual(
            subject,
            Repository('/tmp', 'git@github.com:bunny/wabbit.git')
        )

    def test_inheritance(self):
        self.assertTrue(issubclass(
            Directory,
            Destination
        ))

    def test_path_cannot_be_empty(self):
        with self.assertRaises(ConfigError) as context:
            Directory('')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path cannot be empty'
        )

    def test_path_must_be_absolute(self):
        with self.assertRaises(ConfigError) as context:
            Directory('foo/bar')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not absolute: foo/bar'
        )

    def test_path_must_be_directory(self):
        with self.assertRaises(ConfigError) as context:
            Directory('/tmp/foo')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path is not a directory: /tmp/foo'
        )

    def test_path_has_tilde(self):
        subject = Directory('~/backup')

        self.assertEqual(
            subject._path,
            os.path.expanduser('~/backup')
        )

    def test_backup(self):
        FileSystem.write_file('~/.bunny', 'I am a bunny')

        subject = Directory('~/backup')
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

        subject = Directory('~/backup')
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
        subject = Repository(
            '/tmp',
            'git@github.com:jigarius/clibato.git',
            'backup',
            'Jigarius',
            'jigarius@example.com',
        )

        self.assertIsInstance(subject, Repository)

    def test__eq__(self):
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
        self.assertTrue(issubclass(
            Repository,
            Directory
        ))

    def test_path_cannot_be_empty(self):
        with self.assertRaises(ConfigError) as context:
            Repository('', 'git@github.com:jigarius/clibato.git')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Path cannot be empty'
        )

    def test_remote_cannot_be_empty(self):
        with self.assertRaises(ConfigError) as context:
            Repository('/tmp', '')

        self.assertEqual(
            str(context.exception).strip("'"),
            'Remote cannot be empty'
        )

    def test_default_values_merged(self):
        subject = Repository(
            '/tmp',
            'git@github.com:jigarius/clibato.git'
        )

        self.assertEqual(subject._branch, 'main')
        self.assertEqual(subject._author.name, 'Clibato')
        self.assertEqual(subject._author.email, 'clibato@jigarius.com')

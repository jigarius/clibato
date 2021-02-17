from pathlib import Path
import tempfile
import unittest

from clibato import Content, ConfigError, Destination, Directory, Repository
from .support import TestCase, FileSystem


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
            'path': tempfile.gettempdir()
        })

        self.assertEqual(
            subject,
            Directory(path=tempfile.gettempdir())
        )

    def test_from_dict_with_illegal_type(self):
        """.from_dict() fails with an invalid dict"""
        with self.assertRaisesRegex(ConfigError, 'Illegal type: foobar'):
            Destination.from_dict({'type': 'foobar'})

    def test_from_dict_with_arg_mismatch(self):
        """.from_dict() fails with on argument mismatch"""
        with self.assertRaises(ConfigError) as context:
            Destination.from_dict({
                'type': 'directory',
                'remote': 'git@github.com:jigarius/clibato.git'
            })

        self.assertEqual(
            "__init__() got an unexpected keyword argument 'remote'",
            str(context.exception)
        )


class TestDirectory(TestCase):
    """Test destination.Directory"""

    def test_new(self):
        """Instance creation."""
        subject = Directory(path=tempfile.gettempdir())

        self.assertIsInstance(subject, Directory)

    def test__eq__(self):
        """__eq__()"""
        subject = Directory(path=tempfile.gettempdir())

        self.assertEqual(subject, Directory(path=tempfile.gettempdir()))

        self.assertNotEqual(subject, Directory(path=str(Path.home())))

        self.assertNotEqual(
            subject,
            Repository(tempfile.gettempdir(), 'git@github.com:bunny/wabbit.git')
        )

    def test_inheritance(self):
        """Directory must extend Destination"""
        self.assert_is_subclass(Directory, Destination)

    def test_path(self):
        """.path()"""
        subject = Directory(tempfile.gettempdir())

        self.assertEqual(Path(tempfile.gettempdir()), subject.path())

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
        """Path must be a directory that exists"""
        message = 'Path is not a directory: /tmp/foo'
        with self.assertRaisesRegex(ConfigError, message):
            Directory('/tmp/foo')

    def test_path_has_tilde(self):
        """Path can contain tilde (~)"""
        backup_path = Path.home() / 'backup'
        backup_path.mkdir(exist_ok=True)
        subject = Directory(str(backup_path))

        self.assertEqual(Path('~', 'backup').expanduser(), subject.path())

        backup_path.rmdir()

    def test_backup(self):
        """.backup()"""
        source_dir = tempfile.TemporaryDirectory()
        source_path = Path(source_dir.name)

        backup_dir = tempfile.TemporaryDirectory()
        backup_path = Path(backup_dir.name)

        bunny_path = '.bunny'
        wabbit_path = str(Path('hole', '.wabbit'))

        FileSystem.write_file(source_path / bunny_path, 'I am a bunny')
        FileSystem.write_file(source_path / wabbit_path, 'I am a wabbit')

        subject = Directory(backup_dir.name)
        with self.assertLogs('clibato', None) as context:
            subject.backup([
                Content(bunny_path, source_path / bunny_path),
                Content(wabbit_path, source_path / wabbit_path)
            ])

        self.assert_length(context.records, 2)
        self.assert_log_record(
            context.records[0],
            level='INFO',
            message="Backed up: %s" % (source_path / bunny_path)
        )
        self.assert_log_record(
            context.records[1],
            level='INFO',
            message="Backed up: %s" % (source_path / wabbit_path)
        )

        self.assert_file_contents(backup_path / bunny_path, 'I am a bunny')
        self.assert_file_contents(backup_path / wabbit_path, 'I am a wabbit')

    def test_backup_file_not_found(self):
        """.backup() logs and continues if a file is not found"""
        source_dir = tempfile.TemporaryDirectory()
        source_path = Path(source_dir.name)

        backup_dir = tempfile.TemporaryDirectory()
        backup_path = Path(backup_dir.name)

        bunny_path = '.bunny'
        wabbit_path = str(Path('hole', '.wabbit'))

        FileSystem.write_file(source_path / wabbit_path, 'I am a wabbit')

        subject = Directory(backup_dir.name)
        with self.assertLogs('clibato', None) as context:
            subject.backup([
                Content('.bunny', source_path / bunny_path),
                Content(wabbit_path, source_path / 'hole' / '.wabbit')
            ])

        self.assert_length(context.records, 2)
        self.assert_log_record(
            context.records[0],
            level='ERROR',
            message="[Errno 2] No such file or directory: '%s'" % (source_path / bunny_path)
        )
        self.assert_log_record(
            context.records[1],
            level='INFO',
            message="Backed up: %s" % (source_path / wabbit_path)
        )

        self.assert_file_not_exists(backup_path / bunny_path)
        self.assert_file_contents(backup_path / wabbit_path, 'I am a wabbit')

    def test_restore(self):
        """.restore()"""
        source_dir = tempfile.TemporaryDirectory()
        source_path = Path(source_dir.name)

        backup_dir = tempfile.TemporaryDirectory()
        backup_path = Path(backup_dir.name)

        bunny_path = '.bunny'
        wabbit_path = str(Path('hole', '.wabbit'))

        FileSystem.write_file(backup_path / bunny_path, 'I am a bunny')
        FileSystem.write_file(backup_path / wabbit_path, 'I am a wabbit')

        subject = Directory(backup_dir.name)
        with self.assertLogs('clibato', None) as context:
            subject.restore([
                Content(bunny_path, source_path / bunny_path),
                Content(wabbit_path, source_path / wabbit_path)
            ])

        self.assert_length(context.records, 2)
        self.assert_log_record(
            context.records[0],
            level='INFO',
            message="Restored: %s" % (source_path / bunny_path)
        )
        self.assert_log_record(
            context.records[1],
            level='INFO',
            message="Restored: %s" % (source_path / wabbit_path)
        )

        self.assert_file_contents(source_path / bunny_path, 'I am a bunny')
        self.assert_file_contents(source_path / wabbit_path, 'I am a wabbit')

    def test_restore_file_not_found(self):
        """.restore() logs and continues if a file is not found"""
        source_dir = tempfile.TemporaryDirectory()
        source_path = Path(source_dir.name)

        backup_dir = tempfile.TemporaryDirectory()
        backup_path = Path(backup_dir.name)

        bunny_path = '.bunny'
        wabbit_path = str(Path('hole', '.wabbit'))

        FileSystem.write_file(backup_path / wabbit_path, 'I am a wabbit')

        subject = Directory(backup_dir.name)
        with self.assertLogs('clibato', None) as context:
            subject.restore([
                Content(bunny_path, source_path / bunny_path),
                Content(wabbit_path, source_path / wabbit_path)
            ])

        self.assert_length(context.records, 2)
        self.assert_log_record(
            context.records[0],
            level='ERROR',
            message="[Errno 2] No such file or directory: '%s'" % (backup_path / bunny_path)
        )
        self.assert_log_record(
            context.records[1],
            level='INFO',
            message="Restored: %s" % (source_path / wabbit_path)
        )

        self.assert_file_not_exists(source_path / bunny_path)
        self.assert_file_contents(source_path / wabbit_path, 'I am a wabbit')


class TestRepository(TestCase):
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
        subject = Repository(tempfile.gettempdir(), 'git@github.com:bunny/wabbit.git')

        self.assertEqual(
            subject,
            Repository(tempfile.gettempdir(), 'git@github.com:bunny/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Repository(tempfile.gettempdir(), 'git@github.com:bucky/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Directory(tempfile.gettempdir())
        )

    def test_inheritance(self):
        """Repository must extend Directory"""
        self.assert_is_subclass(Repository, Destination)

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

    @unittest.skip('TODO')
    def test_backup(self):
        """.backup()"""

    @unittest.skip('TODO')
    def test_restore(self):
        """.backup()"""

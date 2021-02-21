from pathlib import Path
from tempfile import gettempdir
import unittest

from clibato import Content, ConfigError, Destination, Directory, Repository
from .support import TestCase


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
            'path': gettempdir()
        })

        self.assertEqual(
            subject,
            Directory(path=gettempdir())
        )

    def test_from_dict_with_illegal_type(self):
        """.from_dict() fails with an invalid dict"""
        with self.assertRaisesRegex(ConfigError, 'Illegal type: foobar'):
            Destination.from_dict({'type': 'foobar'})

    def test_from_dict_with_arg_mismatch(self):
        """.from_dict() fails with on argument mismatch"""
        with self.assertRaises(ConfigError) as cm:
            Destination.from_dict({
                'type': 'directory',
                'remote': 'git@github.com:jigarius/clibato.git'
            })

        self.assertEqual(
            "__init__() got an unexpected keyword argument 'remote'",
            str(cm.exception)
        )


class TestDirectory(TestCase):
    """Test destination.Directory"""

    def test_new(self):
        """Instance creation."""
        subject = Directory(path=gettempdir())

        self.assertIsInstance(subject, Directory)

    def test__eq__(self):
        """__eq__()"""
        subject = Directory(path=gettempdir())

        self.assertEqual(subject, Directory(path=gettempdir()))

        self.assertNotEqual(subject, Directory(path=str(Path.home())))

        self.assertNotEqual(
            subject,
            Repository(gettempdir(), 'git@github.com:bunny/wabbit.git')
        )

    def test_inheritance(self):
        """Directory must extend Destination"""
        self.assert_is_subclass(Directory, Destination)

    def test_path(self):
        """.path()"""
        subject = Directory(gettempdir())

        self.assertEqual(Path(gettempdir()), subject.path())

    def test_path_cannot_be_empty(self):
        """Path cannot be empty"""
        with self.assertRaisesRegex(ConfigError, 'Path cannot be empty'):
            Directory('')

    def test_path_must_be_absolute(self):
        """Path must be absolute"""
        path = Path('foo', 'bar')
        with self.assertRaises(ConfigError) as cm:
            Directory(str(path))

        self.assertEqual(
            f'Path is not absolute: {path}',
            str(cm.exception).strip("'")
        )

    def test_path_must_be_directory(self):
        """Path must be a directory that exists"""
        path = Path(gettempdir(), 'foo').resolve()
        with self.assertRaises(ConfigError) as cm:
            Directory(path=str(path))

        self.assertEqual(
            f'Path is not a directory: {path}',
            str(cm.exception).strip("'")
        )

    def test_path_has_tilde(self):
        """Path can contain tilde (~)"""
        backup_path = Path.home() / 'backup'
        backup_path.mkdir(exist_ok=True)
        subject = Directory(str(backup_path))

        self.assertEqual(Path('~', 'backup').expanduser(), subject.path())

        backup_path.rmdir()

    def test_backup(self):
        """.backup()"""
        source_path, backup_path = self.create_file_fixtures(location='source')
        subject = Directory(path=str(backup_path))

        with self.assertLogs('clibato', None) as cm:
            subject.backup([
                Content(self.BUNNY_PATH, source_path / self.BUNNY_PATH),
                Content(self.WABBIT_PATH, source_path / self.WABBIT_PATH)
            ])

        self.assert_length(cm.records, 2)
        self.assert_log_record(
            cm.records[0],
            level='INFO',
            message=f'Backed up: {source_path / self.BUNNY_PATH}'
        )
        self.assert_log_record(
            cm.records[1],
            level='INFO',
            message=f'Backed up: {source_path / self.WABBIT_PATH}'
        )

        self.assert_file_contents(backup_path / self.BUNNY_PATH, 'I am a bunny')
        self.assert_file_contents(backup_path / self.WABBIT_PATH, 'I am a wabbit')

    def test_backup_file_not_found(self):
        """.backup() logs and continues if a file is not found"""
        source_path, backup_path = self.create_file_fixtures(location='source')
        skunk_path = '.skunk'
        subject = Directory(path=str(backup_path))

        with self.assertLogs('clibato', None) as cm:
            subject.backup([
                Content(skunk_path, source_path / skunk_path),
                Content(self.WABBIT_PATH, source_path / self.WABBIT_PATH)
            ])

        self.assert_length(cm.records, 2)
        self.assert_log_record(
            cm.records[0],
            level='ERROR',
            message=f"[Errno 2] No such file or directory: '{source_path / skunk_path}'"
        )
        self.assert_log_record(
            cm.records[1],
            level='INFO',
            message=f'Backed up: {source_path / self.WABBIT_PATH}'
        )

        self.assert_file_not_exists(backup_path / skunk_path)
        self.assert_file_contents(backup_path / self.WABBIT_PATH, 'I am a wabbit')

    def test_restore(self):
        """.restore()"""
        source_path, backup_path = self.create_file_fixtures(location='backup')
        subject = Directory(path=str(backup_path))

        with self.assertLogs('clibato', None) as cm:
            subject.restore([
                Content(self.BUNNY_PATH, source_path / self.BUNNY_PATH),
                Content(self.WABBIT_PATH, source_path / self.WABBIT_PATH)
            ])

        self.assert_length(cm.records, 2)
        self.assert_log_record(
            cm.records[0],
            level='INFO',
            message=f'Restored: {source_path / self.BUNNY_PATH}'
        )
        self.assert_log_record(
            cm.records[1],
            level='INFO',
            message=f'Restored: {source_path / self.WABBIT_PATH}'
        )

        self.assert_file_contents(source_path / self.BUNNY_PATH, 'I am a bunny')
        self.assert_file_contents(source_path / self.WABBIT_PATH, 'I am a wabbit')

    def test_restore_file_not_found(self):
        """.restore() logs and continues if a file is not found"""
        source_path, backup_path = self.create_file_fixtures(location='backup')
        skunk_path = '.skunk'
        subject = Directory(path=str(backup_path))

        with self.assertLogs('clibato', None) as cm:
            subject.restore([
                Content(skunk_path, source_path / skunk_path),
                Content(self.WABBIT_PATH, source_path / self.WABBIT_PATH)
            ])

        self.assert_length(cm.records, 2)
        self.assert_log_record(
            cm.records[0],
            level='ERROR',
            message=f"[Errno 2] No such file or directory: '{backup_path / skunk_path}'"
        )
        self.assert_log_record(
            cm.records[1],
            level='INFO',
            message=f'Restored: {source_path / self.WABBIT_PATH}'
        )

        self.assert_file_not_exists(source_path / skunk_path)
        self.assert_file_contents(source_path / self.WABBIT_PATH, 'I am a wabbit')


class TestRepository(TestCase):
    """Test destination.Repository"""

    def test_new(self):
        """Instance creation."""
        subject = Repository(
            gettempdir(),
            'git@github.com:jigarius/clibato.git',
            'backup',
            'Jigarius',
            'jigarius@example.com',
        )

        self.assertIsInstance(subject, Repository)

    def test__eq__(self):
        """__eq__()"""
        subject = Repository(gettempdir(), 'git@github.com:bunny/wabbit.git')

        self.assertEqual(
            subject,
            Repository(gettempdir(), 'git@github.com:bunny/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Repository(gettempdir(), 'git@github.com:bucky/wabbit.git')
        )

        self.assertNotEqual(
            subject,
            Directory(gettempdir())
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
            Repository(gettempdir(), '')

    @unittest.skip('TODO')
    def test_backup(self):
        """.backup()"""

    @unittest.skip('TODO')
    def test_restore(self):
        """.backup()"""

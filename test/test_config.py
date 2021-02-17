from shutil import copyfile
from pathlib import Path
import os
import tempfile
import unittest

from clibato import Clibato, Content, Directory, Config, ConfigError
from .support import TestCase


class TestConfig(TestCase):
    """Test clibato.Config"""

    _FIXTURE_PATH = Path(__file__).parent / 'fixtures' / 'clibato.test.yml'

    def test__eq__(self):
        """.__eq__()"""
        subject = Config(
            contents=[Content('.bashrc'), Content('.zshrc')],
            destination=Directory(path=tempfile.gettempdir())
        )

        self.assertEqual(
            subject,
            Config(
                contents=[Content('.bashrc'), Content('.zshrc')],
                destination=Directory(path=tempfile.gettempdir())
            )
        )

        # Difference in contents
        self.assertNotEqual(
            subject,
            Config(
                contents=[Content('.bashrc'), Content('.todo.txt')],
                destination=Directory(path=tempfile.gettempdir())
            ),
        )

        # Difference in destination
        tempdir = tempfile.TemporaryDirectory()
        self.assertNotEqual(
            subject,
            Config(
                contents=[Content('.bashrc'), Content('.zshrc')],
                destination=Directory(path=tempdir.name)
            )
        )

    def test_from_dict(self):
        """.from_dict() works with a valid dict"""
        self.assertEqual(
            TestConfig._build_config(),
            Config.from_dict({
                'contents': {
                    '.bashrc': None,
                    '.zshrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': tempfile.gettempdir()
                }
            })
        )

    def test_from_dict_cannot_contain_illegal_keys(self):
        """.from_dict() fails if when extra keys are found"""
        message = 'Config has illegal keys: bar, foo'
        with self.assertRaisesRegex(ConfigError, message):
            Config.from_dict({
                'foo': 'bunny',
                'bar': 'wabbit',
                'contents': {
                    '.bashrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': tempfile.gettempdir()
                }
            })

    def test_from_dict_cannot_have_missing_keys(self):
        """.from_dict() fails if required keys are missing"""
        message = 'Config has missing keys: contents, destination'
        with self.assertRaisesRegex(ConfigError, message):
            Config.from_dict({})

    def test_from_dict_values_must_be_dictionary(self):
        """.from_dict() fails if values are not dictionaries"""
        for key in ['contents', 'destination']:
            data = {
                'contents': {
                    '.bashrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': tempfile.gettempdir()
                }
            }
            data[key] = 'oops'

            message = f'Config has illegal value for: {key}'
            with self.assertRaisesRegex(ConfigError, message):
                Config.from_dict(data)

    @unittest.skipIf(os.name == 'nt', 'Fixture contains posix paths only')
    def test_from_file(self):
        """.from_file()"""
        with self.assertLogs('clibato') as context:
            self.assertEqual(
                Config(
                    contents=[Content('.bashrc'), Content('.zshrc')],
                    destination=Directory(path='/tmp')
                ),
                Config.from_file(self._FIXTURE_PATH)
            )

        self.assert_length(context.records, 1)
        self.assert_log_record(
            context.records[0],
            level='INFO',
            message=f'Loading configuration: {self._FIXTURE_PATH}'
        )

    def test_from_file_with_non_existent_file(self):
        """.from_file() fails for if file doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            config_file = tempfile.NamedTemporaryFile(suffix='.clibato.yml')
            config_file.close()

            self.assert_file_not_exists(config_file.name)
            self.assertEqual(
                TestConfig._build_config(),
                Config.from_file(config_file.name)
            )

    def test_locate_with_absolute_path(self):
        """.locate() can detect config with absolute paths"""
        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(self._FIXTURE_PATH)
        )

    def test_locate_with_relative_path(self):
        """.locate() can detect config with relative paths"""
        old_cwd = self.chdir(Clibato.ROOT / 'test')

        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(Path('fixtures', 'clibato.test.yml'))
        )

        self.chdir(old_cwd)

    def test_locate_with_home_path(self):
        """.locate() can detect config with ~/ paths"""
        path = Path.home() / 'clibato.test.yml'
        copyfile(self._FIXTURE_PATH, path)

        self.assertEqual(
            path,
            Config.locate(Path('clibato.test.yml'))
        )

        path.unlink()

    def test_locate_with_non_existent_file(self):
        """.locate() returns None if config file is not found"""
        self.assertIsNone(Config.locate(Path('tmp', '.clibato.yml')))

    def test_contents(self):
        """.contents()"""
        self.assertEqual(
            TestConfig._build_config().contents(),
            [
                Content('.bashrc'),
                Content('.zshrc')
            ]
        )

    def test_destination(self):
        """.destination()"""
        self.assertEqual(
            Directory(tempfile.gettempdir()),
            TestConfig._build_config().destination()
        )

    @staticmethod
    def _build_config(contents=None, destination=None):
        contents = contents or [
            Content('.bashrc'),
            Content('.zshrc'),
        ]
        destination = destination or Directory(path=tempfile.gettempdir())

        return Config(contents, destination)

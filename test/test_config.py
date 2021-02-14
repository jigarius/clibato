from shutil import copyfile
import os
import unittest

from clibato import Clibato, Content, Directory, Config, ConfigError


class TestConfig(unittest.TestCase):
    """Test clibato.Config"""

    _FIXTURE_PATH = os.path.join(Clibato.ROOT, 'test', 'fixtures', 'clibato.test.yml')

    def test__eq__(self):
        """.__eq__()"""
        subject = Config.from_dict({
            'contents': {
                '.bashrc': None,
                '.zshrc': None
            },
            'destination': {
                'type': 'directory',
                'path': '/tmp',
            }
        })

        self.assertEqual(
            subject,
            Config.from_dict({
                'contents': {
                    '.bashrc': None,
                    '.zshrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': '/tmp',
                }
            })
        )

        # Difference in content
        self.assertNotEqual(
            subject,
            Config.from_dict({
                'contents': {
                    '.bashrc': None,
                    '.zshrc': '/tmp/.zshrc'
                },
                'destination': {
                    'type': 'directory',
                    'path': '/tmp',
                }
            })
        )

        # Difference in destination
        self.assertNotEqual(
            subject,
            Config.from_dict({
                'contents': {
                    '.bashrc': None,
                    '.zshrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': '/var',
                }
            })
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
                    'path': '/tmp'
                }
            })
        )

    def test_from_dict_content_entry_cannot_be_dictionary(self):
        """.from_dict() fails if content entry is a dictionary"""
        message = 'Illegal value for contents/.bashrc: {}'
        with self.assertRaisesRegex(ConfigError, message):
            Config.from_dict({
                'contents': {
                    '.bashrc': {}
                },
                'destination': {
                    'type': 'directory',
                    'path': '/tmp'
                }
            })

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
                    'path': '/tmp'
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
                    'path': '/tmp'
                }
            }
            data[key] = 'oops'

            message = f'Config has illegal value for: {key}'
            with self.assertRaisesRegex(ConfigError, message):
                Config.from_dict(data)

    def test_from_file(self):
        """.from_file()"""
        self.assertEqual(
            TestConfig._build_config(),
            Config.from_file(self._FIXTURE_PATH)
        )

    def test_from_file_with_non_existent_file(self):
        """.from_file() fails for if file doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            self.assertEqual(
                TestConfig._build_config(),
                Config.from_file('/tmp/.clibato.yml')
            )

    def test_locate_with_absolute_path(self):
        """.locate() can detect config with absolute paths"""
        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(self._FIXTURE_PATH)
        )

    def test_locate_with_relative_path(self):
        """.locate() can detect config with relative paths"""
        original_cwd = os.getcwd()
        os.chdir(os.path.join(Clibato.ROOT, 'test'))

        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(os.path.join('fixtures', 'clibato.test.yml'))
        )

        os.chdir(original_cwd)

    def test_locate_with_home_path(self):
        """.locate() can detect config with ~/ paths"""
        path = os.path.expanduser('~/clibato.test.yml')
        copyfile(self._FIXTURE_PATH, path)

        self.assertEqual(
            path,
            Config.locate('clibato.test.yml')
        )

        os.remove(path)

    def test_locate_with_non_existent_file(self):
        """.locate() returns None if config file is not found"""
        self.assertIsNone(Config.locate('/tmp/.clibato.yml'))

    def test_absolute_path_with_home_path(self):
        """.absolute_path() converts ~/path to $HOME/path"""
        self.assertEqual(
            os.path.expanduser('~/.clibato.yml'),
            Config.absolute_path('~/.clibato.yml')
        )

    def test_absolute_path_with_relative_path(self):
        """.absolute_path() converts path/to/file to $CWD/path/to/file"""
        self.assertEqual(
            os.path.join(os.getcwd(), '.clibato.yml'),
            Config.absolute_path('.clibato.yml')
        )

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
            Directory('/tmp'),
            TestConfig._build_config().destination()
        )

    @staticmethod
    def _build_config(contents=None, destination=None):
        contents = contents or [
            Content('.bashrc'),
            Content('.zshrc'),
        ]
        destination = destination or Directory('/tmp')

        return Config(contents, destination)

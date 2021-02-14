from shutil import copyfile
import os
import unittest

from clibato import Clibato, Content, Directory, Config, ConfigError


class TestConfig(unittest.TestCase):
    _FIXTURE_PATH = os.path.join(Clibato.ROOT, 'test', 'fixtures', 'clibato.test.yml')

    def test__eq__(self):
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
        self.assertEqual(
            __class__._build_config(),
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
        message = f'Config has missing keys: contents, destination'
        with self.assertRaisesRegex(ConfigError, message):
            Config.from_dict({})

    def test_from_dict_values_must_be_dictionary(self):
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
        self.assertEqual(
            __class__._build_config(),
            Config.from_file(self._FIXTURE_PATH)
        )

    def test_from_file_with_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.assertEqual(
                __class__._build_config(),
                Config.from_file('/tmp/.clibato.yml')
            )

    def test_locate_with_absolute_path(self):
        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(self._FIXTURE_PATH)
        )

    def test_locate_with_relative_path(self):
        original_cwd = os.getcwd()
        os.chdir(os.path.join(Clibato.ROOT, 'test'))

        self.assertEqual(
            self._FIXTURE_PATH,
            Config.locate(os.path.join('fixtures', 'clibato.test.yml'))
        )

        os.chdir(original_cwd)

    def test_locate_with_home_path(self):
        path = os.path.expanduser('~/clibato.test.yml')
        copyfile(self._FIXTURE_PATH, path)

        self.assertEqual(
            path,
            Config.locate('clibato.test.yml')
        )

        os.remove(path)

    def test_locate_with_non_existent_file(self):
        self.assertIsNone(Config.locate('/tmp/.clibato.yml'))

    def test_contents(self):
        self.assertEqual(
            __class__._build_config().contents(),
            [
                Content('.bashrc'),
                Content('.zshrc')
            ]
        )

    def test_destination(self):
        self.assertEqual(
            Directory('/tmp'),
            __class__._build_config().destination()
        )

    @staticmethod
    def _build_config(contents=None, destination=None):
        contents = contents or [
            Content('.bashrc'),
            Content('.zshrc'),
        ]
        destination = destination or Directory('/tmp')

        return Config(contents, destination)

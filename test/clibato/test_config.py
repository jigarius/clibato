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
        with self.assertRaises(ConfigError) as context:
            Config.from_dict({
                'contents': {
                    '.bashrc': {}
                },
                'destination': {
                    'type': 'directory',
                    'path': '/tmp'
                }
            })

        self.assertEqual(
            "Illegal value for contents/.bashrc: {}",
            str(context.exception).strip("'")
        )

    def test_from_dict_cannot_contain_illegal_keys(self):
        with self.assertRaises(ConfigError) as context:
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

        self.assertEqual(
            "Config has illegal keys: bar, foo",
            str(context.exception).strip("'")
        )

    def test_from_dict_cannot_have_missing_keys(self):
        with self.assertRaises(ConfigError) as context:
            Config.from_dict({})

        self.assertEqual(
            f'Config has missing keys: contents, destination',
            str(context.exception).strip("'")
        )

    def test_from_file_with_absolute_path(self):
        self.assertEqual(
            __class__._build_config(),
            Config.from_file(self._FIXTURE_PATH)
        )

    def test_from_file_with_relative_path(self):
        original_cwd = os.getcwd()
        os.chdir(os.path.join(Clibato.ROOT, 'test'))

        self.assertEqual(
            __class__._build_config(),
            Config.from_file(os.path.join('fixtures', 'clibato.test.yml'))
        )

        os.chdir(original_cwd)

    def test_from_file_with_home_path(self):
        path = os.path.expanduser('~/clibato.test.yml')
        copyfile(self._FIXTURE_PATH, path)

        self.assertEqual(
            __class__._build_config(),
            Config.from_file('clibato.test.yml')
        )

        os.remove(path)

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

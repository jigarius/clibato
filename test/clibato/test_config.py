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
            Config.from_dict({
                'contents': {
                    '.bashrc': None,
                    '.zshrc': None
                },
                'destination': {
                    'type': 'directory',
                    'path': '/tmp'
                }
            }),
            __class__._build_config()
        )

    def test_from_dict_with_improper_contents(self):
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
            str(context.exception).strip("'"),
            "Illegal value for contents/.bashrc: {}"
        )

    def test_from_dict_with_illegal_keys(self):
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
            str(context.exception).strip("'"),
            "Config has illegal keys: bar, foo"
        )

    def test_from_dict_with_missing_keys(self):
        required_keys = ['contents', 'destination']

        for key in required_keys:
            with self.assertRaises(ConfigError) as context:
                data = {
                    'contents': {
                        '.bashrc': None
                    },
                    'destination': {
                        'type': 'directory',
                        'path': '/tmp'
                    }
                }
                del data[key]

                Config.from_dict(data)

            self.assertEqual(
                str(context.exception).strip("'"),
                f'Config has missing keys: {key}'
            )

    def test_from_file_with_absolute_path(self):
        self.assertEqual(
            Config.from_file(self._FIXTURE_PATH),
            __class__._build_config()
        )

    def test_from_file_with_relative_path(self):
        original_cwd = os.getcwd()
        os.chdir(os.path.join(Clibato.ROOT, 'test'))

        self.assertEqual(
            Config.from_file(os.path.join('fixtures', 'clibato.test.yml')),
            __class__._build_config()
        )

        os.chdir(original_cwd)

    def test_from_file_with_home_path(self):
        path = os.path.expanduser('~/clibato.test.yml')
        copyfile(self._FIXTURE_PATH, path)

        self.assertEqual(
            Config.from_file('clibato.test.yml'),
            __class__._build_config()
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
            __class__._build_config().destination(),
            Directory('/tmp')
        )

    @staticmethod
    def _build_config(contents=None, destination=None):
        contents = contents or [
            Content('.bashrc'),
            Content('.zshrc'),
        ]
        destination = destination or Directory('/tmp')

        return Config(contents, destination)

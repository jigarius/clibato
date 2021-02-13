from pathlib import Path
import os
import unittest

from clibato import Content, Directory, Config, ConfigError


class TestConfig(unittest.TestCase):
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
        config_path = __file__
        config_path = os.path.dirname(config_path)
        config_path = os.path.dirname(config_path)
        config_path = os.path.join(config_path, 'fixtures', 'clibato.test.yml')

        self.assertEqual(
            Config.from_file(config_path),
            __class__._build_config()
        )

    @unittest.skip('TODO')
    def test_from_file_with_relative_path(self):
        pass

    @unittest.skip('TODO')
    def test_from_file_with_home_path(self):
        pass

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
            Directory({'path': '/tmp'})
        )

    @staticmethod
    def _build_config(contents=None, destination=None):
        contents = contents or [
            Content('.bashrc'),
            Content('.zshrc'),
        ]
        destination = destination or Directory({'path': '/tmp'})

        return Config(contents, destination)

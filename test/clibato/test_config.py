from pathlib import Path
import os
import unittest

from clibato import Content, Directory, Config, ConfigError


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config({
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'path': 'git@github.com:jigarius/clibato.git'
            }
        })

    def test_from_file_with_absolute_path(self):
        config_path = __file__
        config_path = os.path.dirname(config_path)
        config_path = os.path.dirname(config_path)
        config_path = os.path.join(config_path, 'fixtures', 'clibato.test.yml')

        expectation = Config({
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'path': '/tmp/clibato',
                'remote': 'git@github.com:USER/SLUG.git'
            }
        })

        self.assertEqual(
            Config.from_file(config_path),
            expectation
        )

    @unittest.skip('TODO')
    def test_from_file_with_relative_path(self):
        pass

    @unittest.skip('TODO')
    def test_from_file_with_home_path(self):
        pass

    def test_data(self):
        config = Config({
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git',
            }
        })

        self.assertEqual(config.data(), {
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git',
            }
        })

    def test_contents(self):
        expectation = {
            '.bashrc': Content('.bashrc', {})
        }

        self.assertEqual(self.config.contents(), expectation)

    def test_contents_when_undefined(self):
        with self.assertRaises(ConfigError) as context:
            Config({
                'destination': {
                    'type': 'repository',
                    'remote': 'git@github.com:jigarius/clibato.git'
                }
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            "Key cannot be empty: contents"
        )

    def test_destination(self):
        config = Config({
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'directory',
                'path': '/tmp'
            }
        })

        self.assertEqual(
            config.destination(),
            Directory({
                'type': 'directory',
                'path': '/tmp'
            })
        )

    def test_destination_when_undefined(self):
        with self.assertRaises(ConfigError) as context:
            Config({
                'contents': {
                    '.bashrc': {}
                },
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            "Key cannot be empty: destination"
        )

    def test_illegal_keys(self):
        with self.assertRaises(ConfigError) as context:
            Config({
                'foo': 'bunny',
                'bar': 'wabbit',
                'contents': {
                    '.bashrc': {}
                },
                'destination': {
                    'type': 'repository',
                    'remote': 'git@github.com:jigarius/clibato.git'
                }
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            "Config has illegal keys: bar, foo"
        )

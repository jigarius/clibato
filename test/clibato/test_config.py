from pathlib import Path
import os
import unittest
import clibato


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = clibato.Config({
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

        expectation = clibato.Config({
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
            clibato.Config.from_file(config_path),
            expectation
        )

    @unittest.skip('TODO')
    def test_from_file_with_relative_path(self):
        pass

    @unittest.skip('TODO')
    def test_from_file_with_home_path(self):
        pass

    def test_data(self):
        config = clibato.Config({
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
            '.bashrc': clibato.Content('.bashrc', {})
        }

        self.assertEqual(self.config.contents(), expectation)

    def test_contents_when_undefined(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Config({
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
        config = clibato.Config({
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
            clibato.destination.Directory({
                'type': 'directory',
                'path': '/tmp'
            })
        )

    def test_destination_when_undefined(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Config({
                'contents': {
                    '.bashrc': {}
                },
            })

        self.assertEqual(
            str(context.exception).strip("'"),
            "Key cannot be empty: destination"
        )

    def test_illegal_keys(self):
        with self.assertRaises(clibato.ConfigError) as context:
            clibato.Config({
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
            "Illegal keys: bar, foo"
        )

    def test_merge(self):
        dict1 = {
            'a': 'alpha',
            'b': '',
            'd': {
                '1': 'one',
                '2': '',
            },
            'e': 'error',
        }

        dict2 = {
            'a': '',
            'b': 'beta',
            'c': 'charlie',
            'd': {
                '2': 'two',
                '3': 'three'
            },
            'e': 'echo'
        }

        expectation = {
            'a': 'alpha',  # Keeps dict1 value since dict2 value is empty.
            'b': 'beta',
            'c': 'charlie',
            'd': {
                '1': 'one',
                '2': 'two',
                '3': 'three'
            },
            'e': 'echo'
        }

        self.assertEqual(
            clibato.Config.merge(dict1, dict2),
            expectation
        )

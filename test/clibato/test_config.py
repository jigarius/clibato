from pathlib import Path
import os
import unittest
import clibato


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = clibato.Config({
            'settings': {
                'workdir': '/tmp/clibato'
            },
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git'
            }
        })

    def test_from_file_with_absolute_path(self):
        config_path = __file__
        for i in range(3):
            config_path = os.path.dirname(config_path)
        config_path = os.path.join(config_path, 'misc', '.clibato.default.yml')

        expectation = clibato.Config({
            'settings': {
                'workdir': '/tmp/clibato'
            },
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:USER/SLUG.git'
            }
        })

        print(expectation.__dict__)
        print(clibato.Config.from_file(config_path).__dict__)

        self.assertEqual(
            clibato.Config.from_file(config_path),
            expectation
        )

    def test_from_file_with_relative_path(self):
        pass

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
            'settings': {
                'workdir': '~/.clibato'
            },
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git',
            }
        })

    def test_workdir(self):
        self.assertEqual(self.config.workdir(), '/tmp/clibato')

    def test_workdir_when_undefined(self):
        config = clibato.Config({
            'contents': {
                '.bashrc': {}
            },
            'destination': {
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git',
            }
        })
        self.assertEqual(config.workdir(), '~/.clibato')

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
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git'
            }
        })

        self.assertEqual(
            config.destination(),
            clibato.destination.Repository({
                'type': 'repository',
                'remote': 'git@github.com:jigarius/clibato.git'
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
        pass

    def test_extract(self):
        pass

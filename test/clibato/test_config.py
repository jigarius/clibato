import unittest
import clibato


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = clibato.config.Config({
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

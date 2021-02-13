import unittest
import os

from clibato import utils


class TestUtils(unittest.TestCase):
    def test_dict_merge(self):
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
            utils.dict_merge(dict1, dict2),
            expectation
        )

    def test_normalize_path(self):
        """Path ~/foo/bar becomes $HOME/foo/bar"""
        self.assertEqual(
            utils.normalize_path('~/foo/bar'),
            os.path.expanduser('~/foo/bar')
        )

    @unittest.skip('Create TestEnsureShape')
    def test_ensure_shape(self):
        pass

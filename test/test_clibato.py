import unittest
from clibato import Clibato
from .support import TestCase


class TestClibato(TestCase):
    """Test Clibato"""

    def test_parse_args_action(self):
        """.parse_args() can parse all possible actions"""
        actions = ['init', 'backup', 'restore', 'version']
        for action in actions:
            args = Clibato.parse_args([action])
            self.assertEqual(action, args.action)

    @unittest.skip('TODO')
    def test_init(self):
        """Test: clibato init"""

    @unittest.skip('TODO')
    def test_backup(self):
        """Test: clibato backup"""

    @unittest.skip('TODO')
    def test_restore(self):
        """Test: clibato backup"""

    @unittest.skip('TODO')
    def test_version(self):
        """Test: clibato backup"""

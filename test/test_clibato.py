from contextlib import redirect_stdout
from os import linesep
from io import StringIO
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

    def test_parse_args_arg_verbose(self):
        """.parse_args() understands the long and short --verbose flag"""
        args = Clibato.parse_args(['version', '--verbose'])
        self.assertEqual(1, args.verbose)

        args = Clibato.parse_args(['version', '-v'])
        self.assertEqual(1, args.verbose)

        args = Clibato.parse_args(['version', '-vv'])
        self.assertEqual(2, args.verbose)

    @unittest.skip('TODO')
    def test_init(self):
        """Test: clibato init"""

    @unittest.skip('TODO')
    def test_backup(self):
        """Test: clibato backup"""

    @unittest.skip('TODO')
    def test_restore(self):
        """Test: clibato restore"""

    def test_version(self):
        """Test: clibato version"""
        stdout = StringIO()
        with redirect_stdout(stdout) as output:
            app = Clibato()
            app.execute(['version'])

        self.assertEqual(f'Clibato v{Clibato.VERSION}\n', output.getvalue())

    def test_version_verbose(self):
        """Test: clibato version --verbose"""
        stdout = StringIO()
        with redirect_stdout(stdout) as output:
            app = Clibato()
            app.execute(['version', '-v'])

        expected = linesep.join([
            "Clibato v%s" % Clibato.VERSION,
            "Author: Jigarius | jigarius.com",
            "GitHub: github.com/jigarius/clibato"
        ]) + linesep

        self.assertEqual(expected, output.getvalue())

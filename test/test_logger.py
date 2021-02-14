import sys
import io
import unittest

from clibato import Logger


class TestLogger(unittest.TestCase):
    """Tests clibato.Logger"""

    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_log_info(self):
        """Test logging an info message"""
        Logger.info('Operation successful.')

        self.assertEqual(
            '[info] Operation successful.\n',
            self.stdout.getvalue()
        )

    def test_log_error(self):
        """Test logging an error message"""
        Logger.error('Operation failed.')

        self.assertEqual(
            '[error] Operation failed.\n',
            self.stdout.getvalue()
        )

    def test_log_debug(self):
        """Test logging a debug message"""
        Logger.debug('Feeding the bunny wabbit.')

        self.assertEqual(
            '[debug] Feeding the bunny wabbit.\n',
            self.stdout.getvalue()
        )

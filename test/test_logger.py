import sys
import io
import unittest

from clibato import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.io = io.StringIO()
        sys.stdout = self.io

    def tearDown(self):
        self.stdout = sys.__stdout__

    def test_log_info(self):
        Logger.info('Operation successful.')

        self.assertEqual(
            '[info] Operation successful.\n',
            self.io.getvalue()
        )

    def test_log_error(self):
        Logger.error('Operation failed.')

        self.assertEqual(
            '[error] Operation failed.\n',
            self.io.getvalue()
        )

    def test_log_debug(self):
        Logger.debug('Feeding the bunny wabbit.')

        self.assertEqual(
            '[debug] Feeding the bunny wabbit.\n',
            self.io.getvalue()
        )

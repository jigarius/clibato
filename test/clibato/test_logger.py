import sys
import io
import unittest

import clibato


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.io = io.StringIO()
        sys.stdout = self.io

    def tearDown(self):
        self.stdout = sys.__stdout__

    def test_log_info(self):
        clibato.Logger.info('Operation successful.')

        self.assertEqual(
            '[info] Operation successful.\n',
            self.io.getvalue()
        )

    def test_log_error(self):
        clibato.Logger.error('Operation failed.')

        self.assertEqual(
            '[error] Operation failed.\n',
            self.io.getvalue()
        )

    def test_log_debug(self):
        clibato.Logger.debug('Feeding the bunny wabbit.')

        self.assertEqual(
            '[debug] Feeding the bunny wabbit.\n',
            self.io.getvalue()
        )

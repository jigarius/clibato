from contextlib import redirect_stdout
from io import StringIO
import logging
from os import linesep
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
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

    def test_parse_args_reads_arg_verbose(self):
        """.parse_args() understands the --verbose and -v arguments"""
        args = Clibato.parse_args(['version', '--verbose'])
        self.assertEqual(1, args.verbose)

        args = Clibato.parse_args(['version', '-v'])
        self.assertEqual(1, args.verbose)

        args = Clibato.parse_args(['version', '-vv'])
        self.assertEqual(2, args.verbose)

    def test_parse_args_reads_arg_config(self):
        """.parse_args() understands the --config and -c arguments"""
        config_path = Path('~', '.clibato.yml')

        args = Clibato.parse_args(['init', '--config', str(config_path)])
        self.assertEqual(config_path, args.config_path)

        args = Clibato.parse_args(['init', '-c', str(config_path)])
        self.assertEqual(config_path, args.config_path)

    def test_init(self):
        """Test: clibato init -c /path/to/.clibato.yml"""
        config_dir = TemporaryDirectory()
        config_path = Path(config_dir.name, '.clibato.yml')

        stdout = StringIO()
        with redirect_stdout(stdout) as output:
            app = Clibato()
            app.execute(['init', '-c', str(config_path)])

        expected = linesep.join([
            f'Configuration created: {config_path}',
            '',
            'Modify the file as per your requirements.',
            'Once done, you can run the following commands.',
            '',
            'clibato backup: Perform a backup.',
            'clibato restore: Restore the last backup.',
            ''
        ])

        self.assertEqual(expected, output.getvalue())

    def test_init_config_file_already_exists(self):
        """Test: clibato init logs error if config file already exists"""
        config_file = NamedTemporaryFile(suffix='.clibato.yml')

        with self.assertLogs('clibato', logging.ERROR) as cm:
            app = Clibato()
            app.execute(['init', '-c', config_file.name])

        self.assert_length(cm.records, 1)
        self.assert_log_record(
            cm.records[0],
            message=f'Configuration already exists: {config_file.name}',
            level='ERROR'
        )


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
            f'Clibato v{Clibato.VERSION}',
            'Author: Jigarius | jigarius.com',
            'GitHub: github.com/jigarius/clibato',
            ''
        ])

        self.assertEqual(expected, output.getvalue())

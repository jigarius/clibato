from contextlib import redirect_stdout
from io import StringIO
import logging
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
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

    def test_config_file_not_found(self):
        """.execute() shows error when config file can't be located"""
        config_path = 'missing.config.yml'

        with self.assertLogs('clibato', logging.ERROR) as cm:
            app = Clibato()
            result = app.execute(['backup', '-c', str(config_path)])

        self.assertFalse(result)
        self.assert_length(cm.records, 1)
        self.assert_log_record(
            cm.records[0],
            level='ERROR',
            message=f'Configuration not found: {config_path}'
        )

    def test_init(self):
        """Test: clibato init -c /path/to/.clibato.yml"""
        config_dir = TemporaryDirectory()
        config_path = Path(config_dir.name, '.clibato.yml')

        stdout = StringIO()
        with redirect_stdout(stdout) as output:
            app = Clibato()
            app.execute(['init', '-c', str(config_path)])

        expected = '\n'.join([
            f'Configuration created: {config_path.resolve()}',
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
        config_path = Path(config_file.name).resolve()

        with self.assertLogs('clibato', logging.ERROR) as cm:
            app = Clibato()
            app.execute(['init', '-c', config_file.name])

        self.assert_length(cm.records, 1)
        self.assert_log_record(
            cm.records[0],
            message=f'Configuration already exists: {config_path}',
            level='ERROR'
        )

    def test_backup(self):
        """Test: clibato backup -v -c /path/to/config.yml"""
        source_path, backup_path = self.create_file_fixtures(location='source')
        config_path = self.create_clibato_config({
            'contents': {
                self.BUNNY_PATH: str(source_path / self.BUNNY_PATH),
                self.WABBIT_PATH: str(source_path / self.WABBIT_PATH)
            },
            'destination': {
                'type': 'directory',
                'path': str(backup_path)
            }
        })

        with self.assertLogs('clibato', logging.INFO) as cm, redirect_stdout(StringIO()) as output:
            app = Clibato()
            app.execute(['backup', '-v', '-c', config_path])

        self.assert_length(cm.records, 3)
        self.assert_log_record(
            cm.records[0],
            level='INFO',
            message=f'Loading configuration: {config_path}'
        )

        self.assert_file_contents(backup_path / self.BUNNY_PATH, 'I am a bunny')
        self.assert_file_contents(backup_path / self.WABBIT_PATH, 'I am a wabbit')

        self.assert_output('Backup completed.\n', output.getvalue())

    def test_restore(self):
        """Test: clibato restore -v -c /path/to/config.yml"""
        source_path, backup_path = self.create_file_fixtures(location='backup')
        config_path = self.create_clibato_config({
            'contents': {
                self.BUNNY_PATH: str(source_path / self.BUNNY_PATH),
                self.WABBIT_PATH: str(source_path / self.WABBIT_PATH)
            },
            'destination': {
                'type': 'directory',
                'path': str(backup_path)
            }
        })

        with self.assertLogs('clibato', logging.INFO) as cm, redirect_stdout(StringIO()) as output:
            app = Clibato()
            app.execute(['restore', '-v', '-c', config_path])

        self.assert_length(cm.records, 3)
        self.assert_log_record(
            cm.records[0],
            level='INFO',
            message=f'Loading configuration: {config_path}'
        )

        self.assert_file_contents(source_path / self.BUNNY_PATH, 'I am a bunny')
        self.assert_file_contents(source_path / self.WABBIT_PATH, 'I am a wabbit')

        expected = '\n'.join(['Restore completed.', ''])
        self.assert_output(expected, output.getvalue())

    def test_version(self):
        """Test: clibato version"""
        with redirect_stdout(StringIO()) as output:
            app = Clibato()
            app.execute(['version'])

        self.assert_output(f'Clibato v{Clibato.VERSION}\n', output.getvalue())

    def test_version_verbose(self):
        """Test: clibato version --verbose"""
        with redirect_stdout(StringIO()) as output:
            app = Clibato()
            app.execute(['version', '-v'])

        expected = '\n'.join([
            f'Clibato v{Clibato.VERSION}',
            'Author: Jigarius | jigarius.com',
            'GitHub: github.com/jigarius/clibato',
            ''
        ])

        self.assert_output(expected, output.getvalue())

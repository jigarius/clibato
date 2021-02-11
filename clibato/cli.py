import argparse
from clibato import Config


class CLI:
    """Clibato CLI"""
    def __init__(self):
        self._args = None
        self._config = None

    def execute(self):
        """Executes the CLI"""
        self._args = CLI._argparser().parse_args()

        if not self._args.action:
            print("Run 'clibato --help' for help.")
            return

        self._log(f'Action: {self._args.action}')
        method = getattr(self, self._args.action)
        method()

    def init(self):
        """Action: Initialize configuration"""
        self._log('TODO: init')

    def backup(self):
        """Action: Create backup"""
        self._log('TODO: backup')

    def restore(self):
        """Action: Restore backup"""
        self._log('TODO: restore')

    def _log(self, message):
        """Logs to STDOUT"""
        if self._args.verbose:
            print('[debug]', message)

    def _ensure_config(self):
        if not self._config:
            self._log(f'Loading configuration: {self._args.config_file}')
            self._config = Config.from_file(self._args.config_file)

    @staticmethod
    def _argparser():
        common_parser = argparse.ArgumentParser(
            add_help=False
        )
        common_parser.add_argument(
            '--verbose',
            default=False,
            action='store_true',
            dest='verbose',
            help='Enable verbose output.'
        )
        common_parser.add_argument(
            '--config-file',
            default='~/.clibato.yml',
            action='store',
            dest='config_file',
            help='A Clibato configuration file (YML).'
        )

        main_parser = argparse.ArgumentParser(
            prog='clibato',
            parents=[common_parser]
        )

        subparsers = main_parser.add_subparsers(dest='action')

        subparsers.add_parser(
            'init',
            help='Initialize configuration',
            parents=[common_parser]
        )

        subparsers.add_parser(
            'backup',
            help='Create backup',
            parents=[common_parser]
        )

        subparsers.add_parser(
            'restore',
            help='Restore backup',
            parents=[common_parser]
        )

        return main_parser

"""Clibato CLI"""

import argparse


class CLI:
    """Clibato CLI"""
    _args = None

    def __init__(self):
        pass

    def execute(self):
        """Executes the CLI"""
        self._args = CLI._argparser().parse_args()
        self.log(f'Action: {self._args.action}')

        method = getattr(self, self._args.action)
        method()

    def init(self):
        """Action: Initialize configuration"""
        self.log('TODO: init')

    def backup(self):
        """Action: Create backup"""
        self.log('TODO: backup')

    def restore(self):
        """Action: Restore backup"""
        self.log('TODO: restore')

    def log(self, message):
        """Logs to STDOUT"""
        if self._args.verbose:
            print('[debug]', message)

    @staticmethod
    def _argparser():
        main_parser = argparse.ArgumentParser(prog='clibato')

        common_parser = argparse.ArgumentParser(add_help=False)
        common_parser.add_argument(
            '--verbose',
            default=False,
            action='store_true',
            dest='verbose',
            help='Enable verbose output.'
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

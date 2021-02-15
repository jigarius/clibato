from shutil import copyfile
import sys
import os
import argparse

from .error import *
from .logger import Logger
from .destination import Destination, Directory, Repository
from .content import Content
from .config import Config


class Clibato:
    """Clibato Controller"""

    ROOT = os.path.dirname(os.path.dirname(__file__))

    def __init__(self):
        self._args = None
        self._config = None

    def execute(self):
        """Executes the CLI"""
        self._args = Clibato._argparser().parse_args()

        if not self._args.action:
            print("Run 'clibato --help' for help.")
            return

        Logger.debug(f'Running action: {self._args.action}')

        try:
            method = getattr(self, self._args.action)
            method()
        except (ConfigError, ActionError) as error:
            Logger.error(error)
            sys.exit(1)

        sys.exit(0)

    def init(self):
        """Action: Initialize configuration"""
        path = Config.absolute_path(self._args.config_file)

        if os.path.isfile(path):
            raise ActionError(f'Configuration already exists: {path}')

        copyfile(
            os.path.join(Clibato.ROOT, '.clibato.example.yml'),
            path
        )

        print('Configuration created: %s' % path)
        print('')
        print('Modify the file as per your requirements.')
        print('Once done, you can run the following commands.')
        print('clibato backup: Perform a backup')
        print('clibato restore: Restore previous backup')

    def backup(self):
        """Action: Create backup"""
        self._ensure_config()

        dest = self._config.destination()
        dest.backup(self._config.contents())

    def restore(self):
        """Action: Restore backup"""
        self._ensure_config()

        dest = self._config.destination()
        dest.restore(self._config.contents())

    def _ensure_config(self):
        if not self._config:
            path = Config.locate(self._args.config_file)
            self._config = Config.from_file(path)

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
            default=Config.DEFAULT_FILENAME,
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

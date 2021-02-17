from shutil import copyfile
from pathlib import Path
import sys
import os
import argparse
import logging

from .error import *
from .destination import Destination, Directory, Repository
from .content import Content
from .config import Config

logger = logging.getLogger('clibato')


class Clibato:
    """Clibato Controller"""

    ROOT = Path(__file__).parent.parent

    def __init__(self):
        self._args = None
        self._config = None

    def execute(self):
        """Executes the CLI"""
        self._args = Clibato._main_argparser().parse_args()

        self._init_logger()

        if not self._args.action:
            print("Run 'clibato --help' for help.")
            return

        logger.debug('Running action: %s', self._args.action)

        try:
            method = getattr(self, self._args.action)
            method()
        except (ConfigError, ActionError) as error:
            logger.error(error)
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

    def _init_logger(self) -> None:
        level = logging.WARNING
        if self._args.verbose:
            level = logging.DEBUG

        logging.basicConfig(
            level=level,
            format="%(levelname)s: %(message)s"
        )

    @staticmethod
    def _main_argparser():
        common_parser = Clibato._common_argparser()
        main_parser = argparse.ArgumentParser(prog='clibato', parents=[common_parser])

        subparsers = main_parser.add_subparsers(dest='action')
        subparsers.add_parser('init', help='Initialize configuration', parents=[common_parser])
        subparsers.add_parser('backup', help='Create backup', parents=[common_parser])
        subparsers.add_parser('restore', help='Restore backup', parents=[common_parser])

        return main_parser

    @staticmethod
    def _common_argparser():
        common_parser = argparse.ArgumentParser(add_help=False)
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

        return common_parser

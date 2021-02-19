from shutil import copyfile
from pathlib import Path
from typing import List, Optional
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
    VERSION = "0.9.0"

    def __init__(self):
        self._args = None

    def execute(self, args=List[str]):
        """Executes the CLI"""
        self._args = Clibato.parse_args(args)
        self._init_logger()
        logger.debug('Received arguments: %s', ' '.join(args))

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

    def init(self):
        """Action: Initialize configuration"""
        path = self._args.config_path.expanduser().resolve()
        if path.is_file():
            raise ActionError(f'Configuration already exists: {path}')

        copyfile(Clibato.ROOT / '.clibato.example.yml', path)

        print('Configuration created: %s' % path)
        print('')
        print('Modify the file as per your requirements.')
        print('Once done, you can run the following commands.')
        print('clibato backup: Perform a backup')
        print('clibato restore: Restore previous backup')

    def backup(self):
        """Action: Create backup"""
        config = self.config()
        dest = config.destination()
        dest.backup(config.contents())

    def restore(self):
        """Action: Restore backup"""
        config = self.config()
        dest = config.destination()
        dest.restore(config.contents())

    def version(self):
        """Action: Version"""
        print(f'Clibato v{self.VERSION}')
        if self._args.verbose:
            print('Author: Jigarius | jigarius.com')
            print('GitHub: github.com/jigarius/clibato')

    def config(self) -> Optional[Config]:
        """
        Get Config based on the --config argument.

        :return: A Config object.
        """
        path = Config.locate(self._args.config_path)
        return Config.from_file(path)

    def _init_logger(self) -> None:
        level = logging.WARNING

        if self._args.verbose == 1:
            level = logging.INFO
        elif self._args.verbose > 1:
            level = logging.DEBUG

        logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    @staticmethod
    def parse_args(args) -> argparse.Namespace:
        """
        Parse CLI arguments, i.e. ARGV.

        Example
        ------
        Clibato.parse_args(sys.argv[1:])

        :param args: CLI arguments, except the program name.
        :return: Arguments parsed with argparse.
        """
        return Clibato._main_argparser().parse_args(args)

    @staticmethod
    def _main_argparser():
        common_parser = Clibato._common_argparser()
        main_parser = argparse.ArgumentParser(
            prog='clibato',
            usage='clibato [-v] [-c ~/.clibato.yml] ACTION',
            parents=[common_parser]
        )

        subparsers = main_parser.add_subparsers(dest='action')
        subparsers.add_parser('init', help='Initialize configuration', parents=[common_parser])
        subparsers.add_parser('backup', help='Create backup', parents=[common_parser])
        subparsers.add_parser('restore', help='Restore backup', parents=[common_parser])
        subparsers.add_parser('version', help='Version information', parents=[common_parser])

        return main_parser

    @staticmethod
    def _common_argparser():
        common_parser = argparse.ArgumentParser(add_help=False)
        common_parser.add_argument(
            '-v',
            '--verbose',
            default=0,
            action='count',
            dest='verbose',
            help='Enable verbose output.'
        )
        common_parser.add_argument(
            '-c',
            '--config',
            type=Path,
            default=Config.DEFAULT_FILENAME,
            action='store',
            dest='config_path',
            help='A Clibato configuration file (YML).'
        )

        return common_parser

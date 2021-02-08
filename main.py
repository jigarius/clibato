#!/usr/bin/env python3

"""
Clibato: CLI Backup Tool.
"""

from clibato.cli import CLI


def main():
    """Clibato Entrypoint"""
    cli = CLI()
    cli.execute()


if __name__ == '__main__':
    main()

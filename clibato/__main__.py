#!/usr/bin/env python3

from sys import argv
from clibato import Clibato


def main():
    """Clibato Entrypoint"""
    app = Clibato()
    app.execute(argv[1:])


if __name__ == '__main__':
    main()

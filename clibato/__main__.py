#!/usr/bin/env python3

import sys
from clibato import Clibato


def main():
    """Clibato Entrypoint"""
    app = Clibato()
    app.execute(sys.argv[1:])
    sys.exit(0)


if __name__ == '__main__':
    main()

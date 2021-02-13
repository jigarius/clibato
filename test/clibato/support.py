import typing
import os
import shutil

from clibato.utils import normalize_path


class FileSystem:
    """File System Helper"""

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def write_file(path, data, append=False) -> type(None):
        path = normalize_path(path)

        mode = 'a' if append else 'w'
        file = open(path, mode)
        file.write(data)
        file.close()

    @staticmethod
    def read_file(path) -> str:
        path = normalize_path(path)

        file = open(path, 'r')
        result = file.read()
        file.close()

        return result

    @staticmethod
    def ensure(dirname: str) -> type(None):
        path = normalize_path(dirname)
        if os.path.isdir(path):
            return

        os.mkdir(path)

    @staticmethod
    def unlink(path: str) -> type(None):
        path = normalize_path(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

import typing
import os
import shutil


class FileSystem:
    """Generic Helper"""

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def write_file(path, data, append=False) -> type(None):
        path = FileSystem.normalize(path)

        mode = 'a' if append else 'w'
        file = open(path, mode)
        file.write(data)
        file.close()

    @staticmethod
    def read_file(path) -> str:
        path = FileSystem.normalize(path)

        file = open(path, 'r')
        result = file.read()
        file.close()

        return result

    @staticmethod
    def ensure(dirname: str) -> type(None):
        path = FileSystem.normalize(dirname)
        if os.path.isdir(path):
            return

        os.mkdir(path)

    @staticmethod
    def unlink(path: str) -> type(None):
        path = FileSystem.normalize(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def normalize(path: str) -> str:
        if path.startswith('~'):
            path = os.path.expanduser(path)

        return path


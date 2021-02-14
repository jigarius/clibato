import os
import shutil


class FileSystem:
    """File System Helper"""

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def write_file(path: str, data: str = '', append=False) -> None:
        """
        Writes data to a file.

        :param path: File path.
        :param data: Data to write.
        :param append: Whether to write in append mode.
        :return: None
        """
        path = os.path.expanduser(path)
        mode = 'a' if append else 'w'

        file = open(path, mode)
        file.write(data)
        file.close()

    @staticmethod
    def read_file(path: str) -> str:
        """
        Read data from a file.

        :param path: File path.
        :return: File contents.
        """
        path = os.path.expanduser(path)

        file = open(path, 'r')
        result = file.read()
        file.close()

        return result

    @staticmethod
    def ensure(path: str) -> None:
        """
        Ensures that the directory exists. If it doesn't exist, it is created.

        Paths starting with ~/ are automatically expanded.

        :param path: Path to directory.
        :return: None
        """
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            return

        os.mkdir(path)

    @staticmethod
    def remove(path: str) -> None:
        """
        Removes the specified file or directory.

        :param path: Path to a file or a directory
        :return: None
        """
        path = os.path.expanduser(path)

        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

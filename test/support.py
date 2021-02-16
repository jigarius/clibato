import os
import shutil
import logging
import unittest


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


class TestCase(unittest.TestCase):
    """Clibato Test Case"""

    def assert_length(self, item, length: int) -> None:
        """
        Assert whether an item has an expected length

        :param item: The item.
        :param length: Expected length.
        :return: None
        """
        self.assertEqual(length, len(item))

    def assert_log_record(self, record: logging.LogRecord, message: str, level: str) -> None:
        """
        Asserts equality of log record properties.

        :param record: A logging.LogRecord.
        :param message: Expected message.
        :param level: Expected level name, e.g. INFO, WARNING, ERROR.
        :return: None
        """
        expectation = {'level': level, 'message': message}
        real = {'level': record.levelname, 'message': record.message}

        self.assertEqual(expectation, real, 'Log record mismatch')

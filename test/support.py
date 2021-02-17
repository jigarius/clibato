from pathlib import Path
import os
import shutil
import logging
import unittest


class FileSystem:
    """File System Helper"""

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def write_file(path: Path, data: str = '', append=False):
        """
        Writes data to a file.

        :param path: File path.
        :param data: Data to write.
        :param append: Whether to write in append mode.
        :return: None
        """
        path = FileSystem._normalize_path(path)
        if not path.parent.is_dir():
            os.makedirs(path.parent)
        mode = 'a' if append else 'w'

        parent = FileSystem._normalize_path(os.path.dirname(path))
        if not parent.is_dir():
            parent.mkdir()

        file = open(path, mode)
        file.write(data)
        file.close()

    @staticmethod
    def read_file(path: Path) -> str:
        """
        Read data from a file.

        :param path: File path.
        :return: File contents.
        """
        path = FileSystem._normalize_path(path)

        file = open(path, 'r')
        result = file.read()
        file.close()

        return result

    @staticmethod
    def remove(path: Path) -> None:
        """
        Removes the specified file or directory.

        :param path: Path to a file or a directory
        :return: None
        """
        path = FileSystem._normalize_path(path)

        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()

    @staticmethod
    def _normalize_path(path) -> Path:
        if not isinstance(path, Path):
            path = Path(path)

        return path.expanduser()


class TestCase(unittest.TestCase):
    """Clibato Test Case"""

    @staticmethod
    def chdir(path: str) -> str:
        """
        Changes the working directory.

        :param path: New CWD.
        :return: Old CWD.
        """
        old_cwd = Path.cwd()
        os.chdir(path)
        return old_cwd

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

    def assert_is_subclass(self, subject, parent):
        """Asserts whether the subject is a subclass of the parent."""
        self.assertTrue(
            issubclass(subject, parent),
            f'{subject} is not a subclass of {parent}'
        )

    def assert_file_exists(self, path: Path) -> None:
        """
        Asserts that the file exists.

        :param path: File path.
        :return: None.
        """
        if not isinstance(path, Path):
            path = Path(path)

        self.assertTrue(path.is_file(), f"Expected file to exist, but it doesn't exist: {path}")

    def assert_file_not_exists(self, path: Path) -> None:
        """
        Asserts that the file doesn't exist.

        :param path: File path.
        :return: None.
        """
        if not isinstance(path, Path):
            path = Path(path)

        self.assertFalse(path.is_file(), f"Expected file to not exist, but it exists: {path}")

    def assert_file_contents(self, path: Path, contents) -> None:
        """
        Asserts whether the file has the expected contents.

        :param path: File path.
        :param contents: Expected contents.
        :return: None.
        """
        self.assert_file_exists(path)
        self.assertEqual(contents, FileSystem.read_file(path))

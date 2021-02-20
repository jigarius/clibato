from contextlib import contextmanager
from pathlib import Path
import os
import logging
from tempfile import NamedTemporaryFile
import unittest
import yaml


class TestCase(unittest.TestCase):
    """Clibato Test Case"""

    @staticmethod
    @contextmanager
    def chdir(path: str) -> str:
        """
        Changes the working directory.

        :param path: New CWD.
        :return: Old CWD.
        """
        old_cwd = Path.cwd()
        os.chdir(path)
        yield
        os.chdir(old_cwd)

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
        self.assertEqual(contents, path.read_text())

    @staticmethod
    def create_clibato_config(data: dict) -> NamedTemporaryFile():
        """
        Creates a temporary YAML containing the provided config.

        :param data: Configuration as a dictionary
        :return: NamedTemporaryFile
        """
        config_file = NamedTemporaryFile(suffix='.clibato.yml')
        with open(config_file.name, 'w') as fh:
            yaml.dump(data, fh)
        return config_file

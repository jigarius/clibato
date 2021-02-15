class Logger:
    """Clibato Logger"""

    _INFO = 'info'
    _ERROR = 'error'
    _DEBUG = 'debug'

    @staticmethod
    def info(message):
        """Logs an info message"""
        Logger._log(message, Logger._INFO)

    @staticmethod
    def error(message):
        """Logs an error message"""
        Logger._log(message, Logger._ERROR)

    @staticmethod
    def debug(message):
        """Logs a debug message"""
        Logger._log(message, Logger._DEBUG)

    @staticmethod
    def _log(message, tipo):
        print(f'[{tipo}] {message}')

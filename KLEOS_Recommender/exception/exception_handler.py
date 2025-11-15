import sys

class AppException(Exception):
    """
    Custom exception class to capture detailed info about exceptions
    such as the script file name and line number where it occurred.
    """

    def __init__(self, error_message: Exception):
        """
        :param error_message: Exception object or string
        """
        super().__init__(error_message)
        self.error_message = self.get_error_message(error_message)

    @staticmethod
    def get_error_message(error: Exception) -> str:
        """
        Prepares a detailed error message including filename and line number.
        """
        _, _, exc_tb = sys.exc_info()  # get current exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown"

        return f"Error occurred in python script [{file_name}], line [{line_number}]: {error}"

    def __repr__(self):
        return f"AppException({self.error_message})"

    def __str__(self):
        return self.error_message

import sys

class CostomException(Exception):
    def __init__(self, message: str, error_detail: Exception = None):
        self.error_message = self.get_detail_error_message(message, error_detail)
        super().__init__(self.error_message)

    def get_detail_error_message(self, message, error_detail):
        _, _, exc_tb = sys.exc_info()

        if exc_tb:
            filename = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno

            return (
                f"{message}\n"
                f"Original error: {repr(error_detail)}\n"
                f"File: {filename}\n"
                f"Line: {line_number}"
            )

        return f"{message} - {repr(error_detail)}"

    def __str__(self):
        return self.error_message
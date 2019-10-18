class YouScanException(Exception):
    def __init__(self, error_code: int, error_message: str, *args):
        super().__init__(*args)
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return f"Code: {self.error_code}, Detail: {self.error_message}"

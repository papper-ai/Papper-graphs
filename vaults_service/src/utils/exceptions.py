class UnsupportedFileType(Exception):
    """Exception raised for unsupported file types."""

    def __init__(self, content_type, message="Unsupported file type"):
        self.content_type = content_type
        self.message = f"{message}: {content_type}"
        super().__init__(self.message)


class EmptyFile(Exception):
    """Exception raised for empty files."""

    def __init__(self, message="Empty file"):
        self.message = f"{message}"
        super().__init__(self.message)
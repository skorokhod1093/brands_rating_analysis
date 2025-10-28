"""Кастомные исключения"""


class AnalyzerError(Exception):
    """Базовое исключение для модуля анализатора"""


class InvalidReportTypeError(AnalyzerError):
    """Исключение возникает при запросе неподдерживаемого типа отчета"""

    def __init__(self, report_type: str):
        super().__init__(f"Unsupported report type: {report_type}")


class FileProcessingError(AnalyzerError):
    """Исключение возникает при обработке файла"""

    def __init__(self, filename: str, message: str):
        super().__init__(f"File processing error '{filename}': {message}")


class DataValidationError(AnalyzerError):
    """Исключение возникает при проверки данных"""

    def __init__(self, message: str):
        super().__init__(f"Incorrect data: {message}")

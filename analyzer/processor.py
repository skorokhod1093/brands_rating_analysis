"""Модуль для обработки одного или нескольких CSV-файлов"""

import csv
from pathlib import Path

from analyzer.models import Product
from analyzer.exceptions import FileProcessingError, DataValidationError


class CSVProcessor:
    """Обрабатывает CSV-файлы"""

    def __init__(self):
        self.products: list[Product] = []

    def read_files(self, file_paths: list[str]) -> list[Product]:
        """Считывает CSV-файлы и возвращает список экземпляров продукта
        Args:
            file_paths: Список путей к CSV-файлам, содержащим данные о продукте
        Returns:
            Список объектов продукта
        """

        for file_path in file_paths:
            self._read_file(file_path)
        return self.products

    def _read_file(self, file_path: str) -> None:
        """Читает один CSV-файл и добавляет продукты в self.products."""
        path = Path(file_path)

        if not path.exists():
            raise FileProcessingError(file_path, "File does not exist")
        if not path.is_file():
            raise FileProcessingError(file_path, "Path is not a file")

        try:
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    raise DataValidationError("The CSV file has no headers")

                for row in reader:
                    product = Product.from_dict(row)
                    self.products.append(product)

        except UnicodeDecodeError as e:
            raise FileProcessingError(
                file_path, "The file is not a CSV file in UTF-8 encoding") from e
        except csv.Error as e:
            raise FileProcessingError(
                file_path, f"Error when parsing a CSV file: {e}") from e

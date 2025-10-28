"""Тесты для модулей анализатора данных: модели, процессор CSV и генераторы отчётов"""

import os
import tempfile

import pytest

from analyzer.exceptions import (
    InvalidReportTypeError,
    FileProcessingError,
    DataValidationError,
)
from analyzer.models import Product
from analyzer.processor import CSVProcessor
from analyzer.reports import ReportFactory, AverageRatingReport


# Фикстуры
@pytest.fixture
def sample_products():
    """Возвращает список продуктов"""

    return [
        Product("iphone 15 pro", "apple", 999.0, 4.9),
        Product("galaxy s23 ultra", "samsung", 1199.0, 4.8),
        Product("redmi note 12", "xiaomi", 199.0, 4.6),
        Product("iphone 14", "apple", 799.0, 4.2),
    ]


@pytest.fixture
def temp_csv_file():
    """Создаёт временный CSV-файл с корректными данными"""

    content = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
iphone 14,apple,799,4.2"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def invalid_csv_file():
    """Создаёт временный CSV-файл с некорректными данными"""

    content = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
invalid_row"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_csv_processor_read_files(temp_csv_file):
    """Тест чтения корректного CSV-файла"""

    processor = CSVProcessor()
    products = processor.read_files([temp_csv_file])

    assert len(products) == 4
    assert products[0].name == "iphone 15 pro"
    assert products[0].brand == "apple"
    assert products[0].price == 999.0
    assert products[0].rating == 4.9


def test_csv_processor_file_not_found():
    """Тест обработки ошибки при отсутствии файла"""
    processor = CSVProcessor()
    with pytest.raises(FileProcessingError):
        processor.read_files(["nonexistent.csv"])


def test_csv_processor_invalid_csv(invalid_csv_file):
    """Тест обработки ошибки при чтении CSV-файла с некорректной структурой"""
    processor = CSVProcessor()
    with pytest.raises(DataValidationError):
        processor.read_files([invalid_csv_file])


def test_csv_processor_missing_columns():
    """Тест обработки ошибки при отсутствии обязательных столбцов в CSV-файле"""
    content = """name,brand,price
iphone 15 pro,apple,999"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write(content)
        temp_path = f.name

    try:
        processor = CSVProcessor()
        with pytest.raises(DataValidationError):
            processor.read_files([temp_path])
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_average_rating_report(sample_products):
    """Тест генерации отчёта со средним рейтингом по брендам"""

    report = AverageRatingReport()
    report_data = report.generate_report(sample_products)

    assert len(report_data) == 3

    apple_rating = next(item for item in report_data if item['brand'] == 'apple')
    assert abs(apple_rating['rating'] - 4.55) < 0.01

    assert report_data[0]['brand'] == 'samsung'
    assert report_data[1]['brand'] == 'xiaomi'
    assert report_data[2]['brand'] == 'apple'


def test_average_rating_report_empty():
    """Тест генерации отчёта со средним рейтингом при пустом списке продуктов"""

    report = AverageRatingReport()
    report_data = report.generate_report([])
    assert len(report_data) == 0


def test_report_factory_create_invalid():
    """Тест обработки ошибки при попытке создать несуществующий тип отчёта"""

    with pytest.raises(InvalidReportTypeError):
        ReportFactory.create_report_generator("invalid-report-type")


@pytest.mark.parametrize(
    "report_type,expected_class",
    [
        ("average-rating", AverageRatingReport),
    ],
)
def test_report_factory_parametrized(report_type, expected_class):
    """Параметризованный тест создания генератора отчёта через фабрику"""

    report_gen = ReportFactory.create_report_generator(report_type)
    assert isinstance(report_gen, expected_class)


@pytest.mark.parametrize("input_data,expected_exception", [
    # ...
    ({"name": "phone", "brand": "test", "price": "not_a_number", "rating": "4.5"},
     DataValidationError),
    ({"name": "phone", "brand": "test", "price": "100", "rating": "invalid_rating"},
     DataValidationError),
    ({"name": "phone", "brand": "test", "price": "100"},
     DataValidationError),
])
def test_product_from_dict(input_data, expected_exception):
    """Параметризованный тест создания Product из словаря"""

    if expected_exception is None:
        product = Product.from_dict(input_data)
        assert isinstance(product, Product)
        assert product.name == input_data["name"]
        assert product.brand == input_data["brand"]
        assert product.price == float(input_data["price"])
        assert product.rating == float(input_data["rating"])
    else:
        with pytest.raises(expected_exception):
            Product.from_dict(input_data)

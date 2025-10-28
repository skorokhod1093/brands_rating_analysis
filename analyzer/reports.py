"""Модуль для создания отчетов"""

from abc import ABC, abstractmethod
from typing import Any, TypedDict

from analyzer.models import Product, BrandRating
from analyzer.exceptions import InvalidReportTypeError


class BrandStats(TypedDict):
    total_rating: float
    count: int


class ReportGenerator(ABC):
    """Абстрактный базовый класс для отчетов"""

    @abstractmethod
    def generate_report(self, products: list[Product]) -> list[dict[str, Any]]:
        """Генерирует отчет из списка продуктов"""


class AverageRatingReport(ReportGenerator):
    """Класс для формирования отчета о среднем рейтинге по брендам"""

    def generate_report(self, products: list[Product]) -> list[dict[str, Any]]:
        """Рассчитывает средний рейтинг для каждого бренда"""
        brand_ratings: dict[str, BrandStats] = {}

        for product in products:
            if product.brand not in brand_ratings:
                brand_ratings[product.brand] = {"total_rating": 0.0, "count": 0}
            brand_ratings[product.brand]["total_rating"] += product.rating
            brand_ratings[product.brand]["count"] += 1

        # Рассчет среднего рейтинга
        results = []
        for brand, data in brand_ratings.items():
            avg_rating = data["total_rating"] / data["count"]
            results.append(BrandRating(brand, avg_rating, data["count"]))

        results.sort(key=lambda x: x.average_rating, reverse=True)

        return [result.to_dict() for result in results]


class ReportFactory:
    """Класс для создания генераторов отчета"""

    _reports = {"average-rating": AverageRatingReport}

    @classmethod
    def create_report_generator(cls, report_type: str) -> ReportGenerator:
        """Создание генератора отчетов на основе типа отчета"""
        if report_type not in cls._reports:
            raise InvalidReportTypeError(report_type)

        return cls._reports[report_type]()

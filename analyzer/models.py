"""Модели данных для анализа продуктов"""

from dataclasses import dataclass
from typing import Any

from analyzer.exceptions import DataValidationError


@dataclass
class Product:
    """Структура данных для получения информации о продукте"""

    name: str
    brand: str
    price: float
    rating: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Product":
        """Создает экземпляр продукта"""

        try:
            return cls(
                name=str(data["name"]),
                brand=str(data["brand"]),
                price=float(data["price"]),
                rating=float(data["rating"]),
            )

        except (KeyError, ValueError, TypeError) as e:
            raise DataValidationError(f"{data}. \n: {e}") from e


@dataclass
class BrandRating:
    """Структура данных для рейтинга бренда"""

    brand: str
    average_rating: float
    product_count: int

    def to_dict(self) -> dict[str, Any]:
        """Преобразование для отображения в таблице"""

        return {"brand": self.brand, "rating": self.average_rating}

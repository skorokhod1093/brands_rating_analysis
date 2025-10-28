"""Интеграционный тест для основного модуля main.py"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
MAIN_SCRIPT = PROJECT_ROOT / "main.py"


@pytest.mark.parametrize(
    "csv_content,expected_in_output",
    [
        ("""name,brand,price,rating
iphone 15 pro,apple,999,4.9
iphone 14,apple,799,4.2""", ["apple"],),
        ("""name,brand,price,rating
pixel 8,google,699,4.7
galaxy s23,samsung,999,4.8""", ["google", "samsung"],),
        ("""name,brand,price,rating
redmi note 12,xiaomi,199,4.6""", ["xiaomi"],),
    ],
)
def test_main_with_different_inputs(csv_content, expected_in_output):
    """Интеграционный параметризованный тест main.py с разными CSV-входами"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        path = f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_SCRIPT),
                "--files",
                path,
                "--report",
                "average-rating",
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=True,  # Автоматически вызывает исключение при ненулевом коде возврата
        )
        # Проверяем, что ожидаемые бренды присутствуют в выводе
        for item in expected_in_output:
            assert (item in result.stdout), f"Ожидаемый элемент '{item}' \
            отсутствует в выводе:\n{result.stdout}"
    finally:
        if os.path.exists(path):
            os.unlink(path)

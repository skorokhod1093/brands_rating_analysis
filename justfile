# Версия для Windows (PowerShell)

# Директория виртуального окружения
VENV := ".venv"

# Создать виртуальное окружение и установить зависимости из requirements.txt
setup:
	python -m venv {{VENV}}
	{{VENV}}/Scripts/python -m pip install --upgrade pip
	{{VENV}}/Scripts/python -m pip install -r requirements.txt

# Запустить все тесты с отчётом о покрытии кода
test:
	{{VENV}}/Scripts/python -m pytest --cov=analyzer --cov-report=term-missing tests/

# Запустить линтер (flake8) для проверки стиля кода
lint:
	{{VENV}}/Scripts/python -m flake8 analyzer/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	{{VENV}}/Scripts/python -m flake8 analyzer/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Отформатировать код с помощью black
format:
	{{VENV}}/Scripts/python -m black analyzer/ tests/

# Проверить типы с помощью mypy
type-check:
	{{VENV}}/Scripts/python -m mypy --check-untyped-defs analyzer/ tests/

run files="" report="average-rating":
    {{VENV}}/Scripts/python main.py --files {{files}} --report {{report}}

# Удалить временные файлы и кэш (сохраняет виртуальное окружение)
clean:
	rm -rf .pytest_cache/ .mypy_cache/ __pycache__/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Полная очистка: удалить всё, включая виртуальное окружение
clean-all: clean
	rm -rf {{VENV}}

# Выполнить все проверки качества кода: линтер, форматтер, типы и тесты
check: lint format type-check test
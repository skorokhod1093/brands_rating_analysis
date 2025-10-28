"""Этот скрипт обрабатывает CSV-файлы, содержащие данные о товаре (название, бренд, цена, рейтинг),
и генерирует отчеты на основе указанного типа отчета"""


import argparse
import sys

from tabulate import tabulate

from analyzer.processor import CSVProcessor
from analyzer.reports import ReportFactory
from analyzer.exceptions import (
    InvalidReportTypeError,
    FileProcessingError,
    DataValidationError,
)


def parse_arguments() -> argparse.Namespace:
    """Разбор аргументов командной строки"""

    parser = argparse.ArgumentParser(description='Analyze brand ratings from CSV files')

    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Paths to CSV files containing product data')

    parser.add_argument(
        '--report',
        required=True,
        choices=['average-rating'],
        help='Type of report to generate')

    return parser.parse_args()

def main() -> None:
    """Основная функция для запуска анализатора"""

    try:
        args = parse_arguments()

        processor = CSVProcessor()
        products = processor.read_files(args.files)

        report_generator = ReportFactory.create_report_generator(args.report)
        report_data = report_generator.generate_report(products)

        if report_data:
            table = tabulate(report_data, headers='keys', tablefmt='grid', floatfmt=".2f")
            print(table)
        else:
            print("No data available to generate report\n")

    except (InvalidReportTypeError, DataValidationError, FileProcessingError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Operation cancelled by user", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

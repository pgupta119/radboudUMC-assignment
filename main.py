from src.components.problem1.logger_setup import setup_logging
from src.components.problem1.excel_converter import ExcelConverter


def main() -> None:
    """Main function to run the ExcelConverter."""
    # Usage
    xls_dir = 'data/source'
    xlsx_dir = 'data/output'
    failed_dir = 'data/failed'

    # Configure logging
    setup_logging()

    # Initialize the ExcelConverter and start batch processing.
    converter = ExcelConverter(xls_dir, xlsx_dir, failed_dir)
    converter.batch_process()


if __name__ == "__main__":
    main()
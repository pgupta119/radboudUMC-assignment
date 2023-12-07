import logging


def setup_logging() -> None:
    """Configure logging settings."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler to log messages to a file.
    file_handler = logging.FileHandler('logs/converter.log')

    # Create a console handler to log messages to the console.
    console_handler = logging.StreamHandler()

    # Define the log message format.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Set the formatter for both handlers.
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
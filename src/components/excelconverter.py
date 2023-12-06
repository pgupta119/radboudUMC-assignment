import logging
import os
import pandas as pd
import shutil


class ExcelConverter:
    def __init__(self, src_directory, dest_directory, failed_directory):
        self.src_directory = src_directory
        self.dest_directory = dest_directory
        self.failed_directory = failed_directory
        self.setup_logging()

    @staticmethod
    def setup_logging():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('../../logs/conversion_log.log')
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    @staticmethod
    def convert_xls_to_xlsx(src_file_path, dest_file_path):
        try:
            df = pd.read_excel(src_file_path, engine='xlrd')
            date_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
            for date_column in date_columns:
                df[date_column] = df[date_column].dt.strftime('%m/%d/%Y')
            df.to_excel(dest_file_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            logging.error(f"Error converting file {src_file_path}: {e}")
            return False

    def batch_process(self, batch_size=10): # Create the directory for failed conversions

        for subdir, _, files in sorted(os.walk(self.src_directory)):
            relative_path = os.path.relpath(subdir, self.src_directory)
            dest_subdir = os.path.join(self.dest_directory, relative_path)
            failed_subdir = os.path.join(self.failed_directory, relative_path)
            os.makedirs(dest_subdir, exist_ok=True)
            os.makedirs(failed_subdir, exist_ok=True)

            xls_files = sorted([f for f in files if f.endswith('.xls')])
            total_files = len(xls_files)

            for i in range(0, total_files, batch_size):
                batch = xls_files[i:i + batch_size]
                for file in batch:
                    src_file_path = os.path.join(subdir, file)
                    dest_file_name = os.path.splitext(file)[0] + '.xlsx'
                    dest_file_path = os.path.join(dest_subdir, dest_file_name)

                    if not os.path.exists(dest_file_path):
                        if not self.convert_xls_to_xlsx(src_file_path, dest_file_path):
                            failed_file_path = os.path.join(failed_subdir, file)
                            shutil.copy(src_file_path, failed_file_path)
                            logging.error(f"Conversion failed for {file}. Moved to failed directory.")
                        else:
                            logging.info(f"Successfully converted {file}")
                    else:
                        logging.info(f"File already converted: {file}")


# Usage
xls_dir = '../../data/source'
xlsx_dir = '../../data/output'
failed_dir = '../../data/failed'
converter = ExcelConverter(xls_dir, xlsx_dir, failed_dir)
converter.batch_process()

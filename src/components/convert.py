import pandas as pd
import os
import logging
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import NamedStyle


# Setup logging with both file and console handlers
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('conversion_log_pandas.log')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


setup_logging()


def convert_xls_to_xlsx(src_file_path, dest_file_path):
    try:
        # Read the xls file using pandas
        df = pd.read_excel(src_file_path, engine='xlrd')

        # Format the date columns to MM/DD/YYYY
        date_columns = [col for col in df.columns if df[col].dtype == 'datetime64[s]']
        for date_column in date_columns:
            df[date_column] = df[date_column].dt.strftime('%m/%d/%Y')

        # Save as xlsx
        df.to_excel(dest_file_path, index=False, engine='openpyxl')
        return True
    except Exception as e:
        logging.error(f"Error converting file {src_file_path}: {e}")
        return False


def convert_xls_to_xlsx(src_file_path, dest_file_path):
    try:
        # Read the xls file using pandas
        df = pd.read_excel(src_file_path, engine='xlrd')

        # Initialize a workbook and sheet
        wb = Workbook()
        ws = wb.active

        # Define a date style for Excel
        date_style = NamedStyle(name='datetime', number_format='YYYY-MM-DD')

        # Apply the dataframe to rows in the worksheet
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                # Apply date style if the value is a datetime
                if isinstance(value, pd.Timestamp):
                    cell.style = date_style

        # Save the workbook
        wb.save(dest_file_path)
        return True
    except Exception as e:
        logging.error(f"Error converting file {src_file_path}: {e}")
        return False


def batch_process(src_directory, dest_directory, batch_size=10):
    for subdir, _, files in sorted(os.walk(src_directory)):
        relative_path = os.path.relpath(subdir, src_directory)
        dest_subdir = os.path.join(dest_directory, relative_path)
        os.makedirs(dest_subdir, exist_ok=True)

        xls_files = sorted([f for f in files if f.endswith('.xls')])
        total_files = len(xls_files)
        for i in range(0, total_files, batch_size):
            batch = xls_files[i:i + batch_size]
            for file in batch:
                src_file_path = os.path.join(subdir, file)
                dest_file_name = os.path.splitext(file)[0] + '.xlsx'
                dest_file_path = os.path.join(dest_subdir, dest_file_name)

                # Check if the file has already been converted
                if not os.path.exists(dest_file_path):
                    if convert_xls_to_xlsx(src_file_path, dest_file_path):
                        logging.info(f"Successfully converted {file}")
                    else:
                        logging.error(f"Conversion failed for {file}")
                else:
                    logging.info(f"File already converted: {file}")


# Directories for source .xls files and output .xlsx files

xls_dir = '../../data/source'
xlsx_dir = '../../data/output/'

batch_process(xls_dir, xlsx_dir)






# import pandas as pd
# import os
# import logging
# from concurrent.futures import ThreadPoolExecutor
#
# class ExcelConverter:
#     def __init__(self, src_directory, dest_directory, batch_size=10):
#         self.src_directory = src_directory
#         self.dest_directory = dest_directory
#         self.batch_size = batch_size
#         self.setup_logging()
#
#     @staticmethod
#     def setup_logging():
#         logger = logging.getLogger()
#         logger.setLevel(logging.INFO)
#
#         file_handler = logging.FileHandler('conversion_log_pandas.log')
#         console_handler = logging.StreamHandler()
#
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#         file_handler.setFormatter(formatter)
#         console_handler.setFormatter(formatter)
#
#         logger.addHandler(file_handler)
#         logger.addHandler(console_handler)
#
#     def convert_xls_to_xlsx(self, src_file_path, dest_file_path):
#         try:
#             df = pd.read_excel(src_file_path, engine='xlrd')
#             df.to_excel(dest_file_path, index=False, engine='openpyxl')
#             return True
#         except Exception as e:
#             logging.error(f"Error converting file {src_file_path}: {e}")
#             return False
#
#     def batch_process(self):
#         with ThreadPoolExecutor() as executor:
#             futures = []
#             for subdir, _, files in os.walk(self.src_directory):
#                 relative_path = os.path.relpath(subdir, self.src_directory)
#                 dest_subdir = os.path.join(self.dest_directory, relative_path)
#                 os.makedirs(dest_subdir, exist_ok=True)
#
#                 xls_files = [f for f in files if f.endswith('.xls')]
#                 for file in xls_files:
#                     src_file_path = os.path.join(subdir, file)
#                     dest_file_name = os.path.splitext(file)[0] + '.xlsx'
#                     dest_file_path = os.path.join(dest_subdir, dest_file_name)
#
#                     if not os.path.exists(dest_file_path):
#                         futures.append(executor.submit(self.convert_xls_to_xlsx, src_file_path, dest_file_path))
#
#             for future in futures:
#                 result = future.result()
#                 if result:
#                     logging.info(f"Successfully converted a {src_file_path} file.")
#                 else:
#                     logging.error(f"Conversion failed for a {src_file_path} file.")
#
# # Usage
# xls_dir = '../../data/source'
# xlsx_dir = '../../data/output'
# converter = ExcelConverter(xls_dir, xlsx_dir)
# converter.batch_process()


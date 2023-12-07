import os
import shutil
import pandas as pd
import logging


class ExcelConverter:
    def __init__(self, src_directory: str, dest_directory: str, failed_directory: str) -> None:
        """Initialize the ExcelConverter instance."""
        self.src_directory = src_directory
        self.dest_directory = dest_directory
        self.failed_directory = failed_directory

    @staticmethod
    def convert_xls_to_xlsx(src_file_path: str, dest_file_path: str) -> bool:
        """Convert .xls file to .xlsx format using pandas."""
        try:
            # Load Excel file into a DataFrame
            df = pd.read_excel(src_file_path, engine='xlrd')

            # Format date columns to 'mm/dd/yyyy'
            date_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
            for date_column in date_columns:
                df[date_column] = df[date_column].dt.strftime('%m/%d/%Y')

            # Save the DataFrame as .xlsx file
            df.to_excel(dest_file_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            logging.error(f"Error converting file {src_file_path}: {e}")
            return False

    def batch_process(self, batch_size: int = 10) -> None:
        """Batch process .xls files in the source directory."""
        for subdir, _, files in sorted(os.walk(self.src_directory)):
            relative_path = os.path.relpath(subdir, self.src_directory)
            dest_subdir = os.path.join(self.dest_directory, relative_path)
            failed_subdir = os.path.join(self.failed_directory, relative_path)

            os.makedirs(dest_subdir, exist_ok=True)
            os.makedirs(failed_subdir, exist_ok=True)

            xls_files = sorted([f for f in files if f.endswith('.xls')])

            for i in range(0, len(xls_files), batch_size):
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


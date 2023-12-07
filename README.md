# RadboudUMC-Assignment

## Problem Statement

The provided dataset contains information on 500 patients, stored in old Excel files with the (.xls) extension. The task is to convert these files in batch to the modern (.xlsx) format.

## Solution

The solution involves using Pandas for converting the files from .xls to .xlsx format. Additionally, the program utilizes the `os` module to execute the conversion process in batch. The status of each conversion is checked to ensure the files are successfully converted.

## Run Code

To run the code, follow these steps:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS:

     ```bash
     source venv/bin/activate
     ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the main script (`main.py`):

   ```bash
   python main.py
   ```
## Problem 1 
We have a data set of 500 patients. However, all the data are stored in the old Excel file type (.xls). Please write a program to convert these files into (.xlsx) in a batch and execute it.

## Source Data

The source data is an example dataset of 500 patients in the .xls format.

## Output

The output will be generated in the 'output' folder in the .xlsx format (within the 'data' folder). Additionally, a log file will be created in the 'logs' folder and displayed in the terminal.

## Problem 2

Data have been extracted from EHR regarding the use of tacrolimus in pediatric solid organ transplant recipients. One of the known side effects of tacrolimus is the decline of renal function over time.

1. To have a better understanding of this problem, we would like you to show us how many patients develop chronic kidney disease.
2. Design and conduct an analysis of the data to determine possible factors contributing to this decline in renal function over time.
3. Is there a dose-response relationship between tacrolimus and renal function? Please design and conduct the analysis.


## Solution
 
1. See the Jupyter Notebook file `src/components/problem2/data_anaylsis.ipynb` for the solution to Problem 2.
2.  Try to make  generic Jupyter Notebook file  `src/components/problem2/generic_code.ipynb` for the solution to Problem 2.
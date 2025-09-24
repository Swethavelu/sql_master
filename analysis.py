import pandas as pd
import os
import re
from typing import List


def read_input(input_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Reads a sheet from the Excel file and filters out rows 
    where 'columnname' is missing.

    Args:
        input_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to read.

    Returns:
        pd.DataFrame: DataFrame containing non-null column names.
    """
    df = pd.read_excel(io=input_path, sheet_name=sheet_name)
    df = df[~df['Column Name'].isna()]
    return df


def get_sql_files(path: str = os.getcwd()) -> List[str]:
    """
    Recursively finds all .sql files in the given path.

    Args:
        path (str, optional): Directory path to search. Defaults to current working directory.

    Returns:
        List[str]: List of absolute paths to SQL files.
    """
    sql_files = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".sql"):
                sql_files.append(os.path.join(root, f))
    return sql_files


def find_columns(sql_files: List[str], df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
    """
    Searches SQL files for the presence and frequency of columns listed in the DataFrame.

    Args:
        sql_files (List[str]): List of SQL file paths.
        df (pd.DataFrame): DataFrame containing column names to search for.
        sheet_name (str): The sheet name (used as column label in the result).

    Returns:
        pd.DataFrame: DataFrame with file names and matching columns with counts.
    """
    result = []

    for sql_file in sql_files:
        column_found = {}

        with open(sql_file, "r", encoding="utf-8") as f:
            query = f.read().lower().replace("\n", " ")

        for _, data in df.iterrows():
            col_name = str(data['Column Name']).lower()
            pattern = fr'(?<![A-Za-z0-9_])(?:\[|"|`)?{re.escape(col_name)}(?:\]|"|`)?(?![A-Za-z0-9_])'

            matches = re.findall(pattern, query)
            if matches:
                column_found[data['Column Name']] = len(matches)  # store counts

        result.append([sql_file, column_found])

    return pd.DataFrame(result, columns=["file_name", sheet_name])



def analyse_fields(sheet_names, xl_path, repo_path):
    
    try:
                                                                           
        dummy = pd.DataFrame(columns=["file_name"])

        for sheet in sheet_names:
            excel_inp = read_input(xl_path, sheet)
            sql_files = get_sql_files(repo_path)
            result = find_columns(sql_files, excel_inp, sheet)

            dummy = pd.merge(dummy, result, on="file_name", how="outer")

        with pd.ExcelWriter(xl_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            dummy.to_excel(writer, sheet_name="result", index=False)

        return True
    
    except Exception as e:
        
        return e
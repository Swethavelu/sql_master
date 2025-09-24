import pandas as pd
import os
import re
from typing import List


def read_input(input_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Reads a sheet from the Excel file and filters rows 
    where 'Change Type' equals 'COL RENAME'.

    Args:
        input_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to read.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows
                      where 'Change Type' is 'COL RENAME'.
    """
    df = pd.read_excel(io=input_path, sheet_name=sheet_name)
    df = df[df['Change Type'] == 'COL RENAME']
    return df


def replace_(df: pd.DataFrame) -> bool:
    """
    Replaces old column names with new names in SQL files.

    Reads each file listed in the DataFrame, replaces all
    occurrences of 'Search Key' with 'Renamed objects', 
    and writes the modified content back to the file.

    Args:
        df (pd.DataFrame): DataFrame with columns:
            - 'Search Key': Old column name to find.
            - 'Renamed objects': New column name to replace with.
            - 'File': Path to the SQL file.

    Returns:
        bool: True if replacements were applied successfully.
    """
    for _, data in df.iterrows():
        old_col = str(data['Search Key'])
        new_col = str(data['Renamed objects'])
        file_path = str(data['File'])

        with open(file_path, "r", encoding="utf-8") as f:
            query = f.read()

        # Regex to safely match column names
        pattern = fr'(?<![A-Za-z0-9_])(?:\[|"|`)?{re.escape(old_col)}(?:\]|"|`)?(?![A-Za-z0-9_])'

        query = re.sub(pattern, new_col, query, flags=re.IGNORECASE)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(query)

    return True


def replace_columns(sheet_names: List[str], xl_path: str) -> bool:
    """
    Orchestrates the column replacement process across multiple sheets.

    For each given sheet:
      1. Reads mapping of old to new column names from the Excel file.
      2. Applies replacements to SQL files listed in the sheet.

    Args:
        sheet_names (List[str]): List of Excel sheet names to process.
        xl_path (str): Path to the Excel file containing mappings.
        repo_path (str): Path to the repository folder containing SQL files.
                        (Currently unused, but can be leveraged for validation).

    Returns:
        bool: True if all replacements succeeded, otherwise exception is returned.
    """
    try:
        for sheet in sheet_names:
            excel_inp = read_input(xl_path, sheet)
            result = replace_(excel_inp)

        return True
    except Exception as e:
        return e
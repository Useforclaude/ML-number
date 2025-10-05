"""
Multi-Format Data Loader for ML Project
Supports CSV, TXT, XLS, XLSX, JSON

By Alex - World-Class AI Expert
"""
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
from typing import Union, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

from src.config import DATA_CONFIG


# ====================================================================================
# MULTI-FORMAT DATA LOADER
# ====================================================================================

def load_data_multi_format(
    file_path: Union[str, Path],
    phone_column: Optional[str] = None,
    price_column: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Load data from multiple file formats

    Supported formats: CSV, TXT, XLS, XLSX, JSON

    Parameters:
    -----------
    file_path : str or Path
        Path to data file
    phone_column : str, optional
        Column name for phone numbers (auto-detected if None)
    price_column : str, optional
        Column name for prices (auto-detected if None)
    **kwargs
        Additional parameters passed to pandas read functions

    Returns:
    --------
    df : pd.DataFrame
        Loaded dataframe

    Examples:
    ---------
    >>> df = load_data_multi_format('data.csv')
    >>> df = load_data_multi_format('data.xlsx', sheet_name='Sheet1')
    >>> df = load_data_multi_format('data.txt', delimiter='|')
    >>> df = load_data_multi_format('data.json')
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Get file extension
    ext = file_path.suffix.lower().lstrip('.')

    print(f"📂 Loading data from: {file_path}")
    print(f"📄 File format: {ext.upper()}")

    # Load based on format
    try:
        if ext == 'csv':
            df = _load_csv(file_path, **kwargs)

        elif ext == 'txt':
            df = _load_txt(file_path, **kwargs)

        elif ext in ['xls', 'xlsx']:
            df = _load_excel(file_path, **kwargs)

        elif ext == 'json':
            df = _load_json(file_path, **kwargs)

        else:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {DATA_CONFIG['supported_formats']}"
            )

        print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")

        return df

    except Exception as e:
        raise Exception(f"Error loading {ext.upper()} file: {str(e)}")


def _load_csv(file_path: Path, **kwargs) -> pd.DataFrame:
    """Load CSV file"""
    # Try different encodings
    encodings = kwargs.pop('encoding', None)
    if encodings is None:
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp874', 'iso-8859-1']
    else:
        encodings = [encodings]

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, **kwargs)
            print(f"   ✅ Encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not decode CSV file with any encoding: {encodings}")


def _load_txt(file_path: Path, **kwargs) -> pd.DataFrame:
    """
    Load TXT file

    Tries multiple delimiters: tab, comma, pipe, space
    """
    # Auto-detect delimiter if not specified
    delimiter = kwargs.pop('delimiter', None) or kwargs.pop('sep', None)

    if delimiter is None:
        # Try to auto-detect delimiter
        delimiters = ['\t', ',', '|', ';', ' ']

        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        # Count occurrences of each delimiter
        delimiter_counts = {delim: first_line.count(delim) for delim in delimiters}

        # Use the most common delimiter
        delimiter = max(delimiter_counts, key=delimiter_counts.get)
        print(f"   🔍 Auto-detected delimiter: '{delimiter}'")

    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp874']

    for encoding in encodings:
        try:
            df = pd.read_csv(
                file_path,
                delimiter=delimiter,
                encoding=encoding,
                **kwargs
            )
            print(f"   ✅ Encoding: {encoding}")
            return df
        except:
            continue

    raise ValueError("Could not load TXT file with any delimiter/encoding combination")


def _load_excel(file_path: Path, **kwargs) -> pd.DataFrame:
    """Load Excel file (XLS or XLSX)"""
    # Default to first sheet if not specified
    sheet_name = kwargs.get('sheet_name', 0)

    try:
        df = pd.read_excel(file_path, **kwargs)

        # If sheet_name is 0 or None, it's the first sheet
        if sheet_name == 0 or sheet_name is None:
            print(f"   📊 Loaded first sheet")
        else:
            print(f"   📊 Loaded sheet: {sheet_name}")

        return df

    except Exception as e:
        # Try to show available sheets
        try:
            import openpyxl
            wb = openpyxl.load_workbook(file_path, read_only=True)
            sheets = wb.sheetnames
            wb.close()
            raise ValueError(
                f"Error loading Excel: {str(e)}\n"
                f"Available sheets: {sheets}"
            )
        except:
            raise ValueError(f"Error loading Excel: {str(e)}")


def _load_json(file_path: Path, **kwargs) -> pd.DataFrame:
    """
    Load JSON file

    Supports:
    - Array of objects: [{"phone": "0812345678", "price": 5000}, ...]
    - Object with data key: {"data": [...]}
    - Lines format (JSONL): one JSON object per line
    """
    orient = kwargs.pop('orient', None)
    lines = kwargs.pop('lines', False)

    try:
        # Try pandas read_json first
        if orient or lines:
            df = pd.read_json(file_path, orient=orient, lines=lines, **kwargs)
        else:
            # Try different orientations
            for orient_type in ['records', 'index', 'columns']:
                try:
                    df = pd.read_json(file_path, orient=orient_type, **kwargs)
                    print(f"   ✅ JSON orient: {orient_type}")
                    return df
                except:
                    continue

            # Try as JSON Lines
            try:
                df = pd.read_json(file_path, lines=True, **kwargs)
                print(f"   ✅ JSON format: Lines (JSONL)")
                return df
            except:
                pass

            # Manual load as fallback
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if data is wrapped in a key
            if isinstance(data, dict):
                # Try common keys
                for key in ['data', 'records', 'rows', 'items']:
                    if key in data:
                        df = pd.DataFrame(data[key])
                        print(f"   ✅ JSON key: {key}")
                        return df

                # If no common key, try to convert dict to DataFrame
                df = pd.DataFrame([data])
            else:
                df = pd.DataFrame(data)

        print(f"   ✅ JSON loaded successfully")
        return df

    except Exception as e:
        raise ValueError(f"Error loading JSON: {str(e)}")


# ====================================================================================
# AUTO-DETECT AND VALIDATE
# ====================================================================================

def validate_data(
    df: pd.DataFrame,
    phone_column: Optional[str] = None,
    price_column: Optional[str] = None,
    auto_fix: bool = True
) -> Tuple[pd.DataFrame, dict]:
    """
    Validate and optionally fix data issues

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    phone_column : str, optional
        Phone number column name
    price_column : str, optional
        Price column name
    auto_fix : bool, default=True
        Automatically fix common issues

    Returns:
    --------
    df_valid : pd.DataFrame
        Validated dataframe
    report : dict
        Validation report
    """
    report = {
        'original_rows': len(df),
        'original_columns': len(df.columns),
        'issues': [],
        'fixes': []
    }

    # Auto-detect columns if not specified
    if phone_column is None:
        phone_column = auto_detect_phone_column(df)
        report['phone_column'] = phone_column

    if price_column is None:
        price_column = auto_detect_price_column(df)
        report['price_column'] = price_column

    # Check for required columns
    if phone_column not in df.columns:
        raise ValueError(f"Phone column '{phone_column}' not found in data")
    if price_column not in df.columns:
        raise ValueError(f"Price column '{price_column}' not found in data")

    df_valid = df.copy()

    # Validate phone numbers
    invalid_phones = ~df_valid[phone_column].astype(str).str.match(r'^\d{10}$')
    if invalid_phones.any():
        count = invalid_phones.sum()
        report['issues'].append(f"{count} invalid phone numbers")

        if auto_fix:
            # Try to fix phone numbers
            df_valid = df_valid[~invalid_phones]
            report['fixes'].append(f"Removed {count} rows with invalid phones")

    # Validate prices
    config = DATA_CONFIG
    price_min = config['price_min']
    price_max = config['price_max']

    invalid_prices = (
        (df_valid[price_column] < price_min) |
        (df_valid[price_column] > price_max) |
        (df_valid[price_column].isna())
    )

    if invalid_prices.any():
        count = invalid_prices.sum()
        report['issues'].append(f"{count} invalid prices")

        if auto_fix:
            df_valid = df_valid[~invalid_prices]
            report['fixes'].append(f"Removed {count} rows with invalid prices")

    # Check for duplicates
    duplicates = df_valid.duplicated(subset=[phone_column])
    if duplicates.any():
        count = duplicates.sum()
        report['issues'].append(f"{count} duplicate phone numbers")

        if auto_fix:
            # Keep first occurrence
            df_valid = df_valid[~duplicates]
            report['fixes'].append(f"Removed {count} duplicate rows")

    report['final_rows'] = len(df_valid)
    report['rows_removed'] = report['original_rows'] - report['final_rows']

    return df_valid, report


def auto_detect_phone_column(df: pd.DataFrame) -> str:
    """Auto-detect phone number column"""
    possible_names = DATA_CONFIG['phone_column_names']

    # Try by column name
    for col in df.columns:
        if any(name in col.lower() for name in possible_names):
            return col

    # Try by data pattern
    for col in df.columns:
        sample = df[col].astype(str).str.replace(r'\D', '', regex=True)
        if (sample.str.len() == 10).sum() > len(df) * 0.8:  # 80% match
            return col

    raise ValueError("Could not auto-detect phone number column")


def auto_detect_price_column(df: pd.DataFrame) -> str:
    """Auto-detect price column"""
    possible_names = DATA_CONFIG['price_column_names']

    # Try by column name
    for col in df.columns:
        if any(name in col.lower() for name in possible_names):
            return col

    # Try by data type (numeric)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 1:
        return numeric_cols[0]
    elif len(numeric_cols) > 1:
        # Use the one with widest range (likely to be price)
        ranges = {col: df[col].max() - df[col].min() for col in numeric_cols}
        return max(ranges, key=ranges.get)

    raise ValueError("Could not auto-detect price column")


# ====================================================================================
# CONVENIENCE FUNCTION
# ====================================================================================

def load_and_validate(
    file_path: Union[str, Path],
    phone_column: Optional[str] = None,
    price_column: Optional[str] = None,
    auto_fix: bool = True,
    verbose: bool = True,
    **kwargs
) -> Tuple[pd.DataFrame, dict]:
    """
    Load data from file and validate in one step

    Parameters:
    -----------
    file_path : str or Path
        Path to data file
    phone_column : str, optional
        Phone column name (auto-detected if None)
    price_column : str, optional
        Price column name (auto-detected if None)
    auto_fix : bool, default=True
        Auto-fix data issues
    verbose : bool, default=True
        Print validation report
    **kwargs
        Additional parameters for file loading

    Returns:
    --------
    df_valid : pd.DataFrame
        Validated dataframe
    report : dict
        Validation report

    Example:
    --------
    >>> df, report = load_and_validate('data.csv')
    >>> print(f"Loaded {len(df)} valid records")
    """
    # Load data
    df = load_data_multi_format(file_path, **kwargs)

    # Validate
    df_valid, report = validate_data(
        df,
        phone_column=phone_column,
        price_column=price_column,
        auto_fix=auto_fix
    )

    # Print report
    if verbose:
        print("\n" + "=" * 80)
        print("📊 VALIDATION REPORT")
        print("=" * 80)
        print(f"Original rows: {report['original_rows']:,}")
        print(f"Final rows: {report['final_rows']:,}")
        print(f"Rows removed: {report['rows_removed']:,}")

        if report['issues']:
            print("\n⚠️  Issues found:")
            for issue in report['issues']:
                print(f"   - {issue}")

        if report['fixes']:
            print("\n✅ Fixes applied:")
            for fix in report['fixes']:
                print(f"   - {fix}")

        print("=" * 80)

    return df_valid, report


# ====================================================================================
# MAIN (for testing)
# ====================================================================================

if __name__ == "__main__":
    # Test multi-format loader
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        df, report = load_and_validate(file_path)
        print(f"\n✅ Successfully loaded {len(df)} records")
        print(f"\nFirst 5 rows:")
        print(df.head())
    else:
        print("Usage: python data_loader.py <file_path>")

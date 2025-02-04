import time
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np


def insert_missing_timestamps(df, timestamp_index, interpolate, sampling_period=3600):
    """
    Insert missing rows in the DataFrame where the difference between consecutive timestamps
    is not equals to the sampling_period. The inserted rows will only have the timestamp column
    filled.
    """
    # Extract timestamps and convert them
    timestamps = df[TIMESTAMP]
    posix_index = df.columns.get_loc(TIMESTAMP)
    df.iloc[:, timestamp_index] = df.iloc[:, timestamp_index].apply(to_date_correct)
    dates = df.iloc[:, timestamp_index]

    # Compute time differences
    diff = timestamps.diff().dropna()

    # Identify missing timestamps
    problematic_rows = diff[diff != sampling_period].index

    # Generate missing rows efficiently
    new_rows = []
    for row in problematic_rows:
        expected_timestamp = timestamps.iloc[row - 1] + sampling_period
        expected_date = dates.iloc[row - 1] + timedelta(hours=1)

        new_row = [np.nan] * df.shape[1]
        new_row[posix_index] = expected_timestamp
        new_row[timestamp_index] = expected_date
        new_rows.append(new_row)

    # Insert missing rows and reindex
    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows, columns=df.columns)], ignore_index=True)
        df = df.sort_values(by=TIMESTAMP).reset_index(drop=True)

    return df


def to_date_correct(date):
    """
    Convert a date string in the format 'MM/DD HH:MM:SS' to a TIMESTAMP timestamp.
    Assumes the current year if no year is provided in the input.
    """
    # Add the current year to the input date for context
    current_year = datetime.now().year
    full_date_str = f"{current_year}/{date.strip()}"

    if date.endswith('24:00:00'):
        date_part = full_date_str.split('  ')[0]
        # Convert to datetime and add one day
        obj_date = datetime.strptime(date_part, '%Y/%m/%d') + timedelta(days=1)
    else:
        obj_date = datetime.strptime(full_date_str, '%Y/%m/%d %H:%M:%S')

    return obj_date


def to_TIMESTAMP(date):
    """
    Convert a date to a TIMESTAMP timestamp.
    """
    return time.mktime(to_date_correct(date).timetuple())


def to_relative_TIMESTAMP(first_date, date):
    """
    Compute the relative TIMESTAMP timestamp difference between two dates.
    """
    return to_TIMESTAMP(date) - first_date


def get_files_with_extension(extension):
    """
    Retrieve a list of files with a given extension in the current directory.
    """
    return [file for file in os.listdir('.') if file.endswith(extension)]


def process_timestamps(df, time_label, interpolate):
    """
    Process timestamps in a DataFrame, converting to TIMESTAMP and inserting missing values.
    """
    first_date = to_TIMESTAMP(df.iloc[0, 0])
    timestamp_index = df.columns.get_loc(time_label)
    df[TIMESTAMP] = df.iloc[:, timestamp_index] \
        .apply(lambda x: to_relative_TIMESTAMP(first_date, x))
    return insert_missing_timestamps(df, timestamp_index, interpolate)


def interpolate_missing_timestamps(df):
    """
    Interpolates missing timestamps in a DataFrame using time-based interpolation.
    """
    df.set_index(DATES, inplace=True)
    df.interpolate(method='time', inplace=True)


def select_relevant_columns(df, prefix, suffix):
    """
    Select relevant columns from a DataFrame based on a prefix and suffix.
    """
    relevant_columns = [TIMESTAMP] + [col for col in df.columns if
                                      (col.startswith(prefix) and col.endswith(suffix))]
    df = df[relevant_columns]
    df.columns = df.columns.str.removesuffix(suffix)
    return df


def merge_sheets(df, prefix, suffix, merged_df):
    """
    Merge multiple sheets into a single DataFrame based on a timestamp column.
    """
    twin_df = select_relevant_columns(df, prefix, suffix)
    # Merge with the main DataFrame
    if merged_df is None:
        # First sheet, initialize the merged DataFrame
        merged = twin_df
    else:
        # Merge on the Date/Time column
        merged = pd.merge(merged_df, twin_df, on=TIMESTAMP, how="outer")
    return merged


def get_output_filename(filename, extension, interpolate, suffix):
    """
    Generates an output filename based on input parameters.

    The function constructs a filename by removing the given extension from
    the original filename, adding a prefix, an optional interpolation flag,
    and a suffix before appending ".csv".
    """
    return f"mrg{'_inter' if interpolate else ''}_{filename[:-len(extension)]}{suffix}.csv"


if __name__ == "__main__":
    TIMESTAMP = 'timestamp(s)'
    DATES = 'dates'

    file_extension = '.xlsx'
    timestamp_label = 'Date/Time'
    dt_suffix = '_module'
    pt_suffix = '_real'

    translation_dict = {
        'Consumo Refrigeración': 'cooling',
        'Consumo Ventilación': 'ventilation',
        'Consumo refrigeración': 'cooling',
        'Consumo ventilación': 'ventilation',
        'Consumo iluminación': 'illumination',
        'Consumo total': 'total'
    }

    interpolation = False

    # Get a list of all Excel files in the current folder
    excel_files = get_files_with_extension(file_extension)

    # Process each Excel file
    for excel_file in excel_files:
        # Initialize an empty DataFrame for the merged result
        merged_dt = None
        merged_pt = None

        # Read all sheets into a dictionary of DataFrames
        sheets = pd.read_excel(excel_file, sheet_name=None)

        # Process each sheet in the file
        for sheet_name, sheet_df in sheets.items():
            # Translate the sheet name
            translated_name = translation_dict.get(sheet_name, sheet_name)

            # Rename columns Real (wh) and Módulo with the sheet name as a prefix
            sheet_df = sheet_df.rename(
                columns={
                    "Real (wh)": f"{translated_name}{pt_suffix}",
                    "Real": f"{translated_name}{pt_suffix}",
                    "Módulo": f"{translated_name}{dt_suffix}",
                    "Cal": f"{translated_name}{dt_suffix}",
                }
            )

            sheet_df = process_timestamps(sheet_df, timestamp_label, interpolation)

            # Select only the relevant columns
            merged_dt = merge_sheets(sheet_df, translated_name, dt_suffix, merged_dt)
            merged_pt = merge_sheets(sheet_df, translated_name, pt_suffix, merged_pt)

        # Save the final merged DataFrame to a CSV file
        merged_dt.to_csv(get_output_filename(excel_file, file_extension, interpolation, '_dt'),
                         index=False, encoding='utf-8')
        merged_pt.to_csv(get_output_filename(excel_file, file_extension, interpolation, '_pt')
                         , index=False, encoding='utf-8')
        print(
            f"All pages merged into {get_output_filename(excel_file, file_extension, interpolation, '')}")

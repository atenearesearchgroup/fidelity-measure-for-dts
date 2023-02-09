import numpy as np
import pandas as pd


def clean_df(df: pd.DataFrame, columns):
    """Turns an array to pandas Dataframe, gets rid of any empty cells, and parse strings to numbers"""
    cleaned_df = pd.DataFrame()
    for c in columns:
        cleaned_df.insert(0, c, df.loc[:, c], True) # Insert columns to the dataframe

    for name, _ in cleaned_df.items():
        cleaned_df[name].replace(' ', np.nan, inplace=True)
        cleaned_df.dropna(subset=[name], inplace=True) # Remove any empty cells
        cleaned_df[name].update(pd.to_numeric(cleaned_df[name], errors='coerce'))  # Parse to numeric format

    return cleaned_df

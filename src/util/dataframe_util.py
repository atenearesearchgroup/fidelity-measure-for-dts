import pandas as pd


def clean_df(df: pd.DataFrame):
    """
    Cleans a pandas DataFrame: gets rid of any empty cells, and parses strings to numbers.
    """
    cleaned_df = df.copy()

    cleaned_df = cleaned_df.apply(pd.to_numeric, errors='coerce')
    for name, _ in cleaned_df.items():
        if cleaned_df[name].dtype == 'bool':
            cleaned_df[name] = cleaned_df[name].astype('float64')
        if cleaned_df[name].isnull().all():
            cleaned_df[name] = cleaned_df[name].fillna(df[name])
    cleaned_df = cleaned_df.dropna()  # Remove any empty cells
    cleaned_df = cleaned_df.reset_index()

    return cleaned_df

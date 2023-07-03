import numpy as np
import pandas as pd
import ruptures as rpt

import statsmodels.api as sm


def get_change_point(df: pd.DataFrame, ordering_params: list, variables: list, number_of_changes: int = 1):
    # Order the dataframe by params
    for param in ordering_params:
        df = df.sort_values(param)

    # Separate the input variables and the output variables
    signals = []
    for v in variables:
        sign = df[v].values
        signals.append(sign)

    # Combine the input signals and response variable into a signal matrix
    signals = np.column_stack(tuple(signals))

    # Perform change point detection
    model = "l2"  # Select the model for change point detection (e.g., "l2", "rbf")
    algo = rpt.Dynp(model=model, min_size=3, jump=5)
    return signals, algo.fit_predict(signals, number_of_changes)


def execute_regression(df: pd.DataFrame, breakpoint: float, param_interest):
    condition = df['percentage_matched_snapshots'] >= breakpoint
    df = df.loc[condition, [f'mad_{param_interest}', 'init_gap', 'cont_gap', 'percentage_matched_snapshots']]

    # Separate the input variables (x) and the output variable (y)
    x = df[['init_gap', 'cont_gap', f'mad_{param_interest}']]
    y = df['percentage_matched_snapshots']

    # Add a constant column to the input variables for the intercept term
    x = sm.add_constant(x)

    # Fit the multiple linear regression model
    model = sm.OLS(y, x)
    results = model.fit()

    return results

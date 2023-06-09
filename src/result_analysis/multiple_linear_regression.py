import os

import pandas as pd
import statsmodels.api as sm


def execute_regression(file):
    # Read the Excel file into a DataFrame
    current_directory = os.path.join(os.getcwd(), '')
    output_directory = current_directory + 'resources/output/evaluation/lift/'
    df = pd.read_excel(output_directory + file, sheet_name='cutBajada_4_0_4Bajada_4_0_4_01')

    if file.find('segment') >= 0:
        breakpoint = 85  # Set the breakpoint for the segment
        condition = df['percentage_matched_snapshots'] > breakpoint
        df = df.loc[condition, ['mad_accel(m/s2)', 'init_gap', 'cont_gap', 'percentage_matched_snapshots']]

    # Separate the input variables (X) and the output variable (Y)
    X = df[['init_gap', 'cont_gap', 'mad_accel(m/s2)']]
    Y = df['percentage_matched_snapshots']

    # Add a constant column to the input variables for the intercept term
    X = sm.add_constant(X)

    # Fit the multiple linear regression model
    model = sm.OLS(Y, X)
    results = model.fit()

    # Extract the relevant coefficients and statistics
    model_name = file.split('.')[0]
    r_squared = results.rsquared
    f_statistic = results.fvalue
    coef_mad = results.params['mad_accel(m/s2)']
    p_value_mad = results.pvalues['mad_accel(m/s2)']
    coef_init_gap = results.params['init_gap']
    p_value_init_gap = results.pvalues['init_gap']
    coef_cont_gap = results.params['cont_gap']
    p_value_cont_gap = results.pvalues['cont_gap']

    # Return the formatted results as a string
    results_str = f"{model_name},{r_squared:.3f},{f_statistic:.3f},{coef_mad:.3f} ± {results.bse['mad_accel(m/s2)']:.3f},{p_value_mad:.3f},{coef_init_gap:.3f} ± {results.bse['init_gap']:.3f},{p_value_init_gap:.3f},{coef_cont_gap:.3f} ± {results.bse['cont_gap']:.3f},{p_value_cont_gap:.3f}"
    return results_str


# List of input file names
file_names = ['cutBajada_4_0_4Bajada_4_0_4_01_affine_gap.xlsx',
              'cutBajada_4_0_4Bajada_4_0_4_01_affine_gap(segment).xlsx',
              'cutBajada_4_0_4Bajada_4_0_4_01_simple_gap.xlsx',
              'cutBajada_4_0_4Bajada_4_0_4_01_simple_gap(segment).xlsx']

# Store the results in a CSV file
output_file = '../regression_results.csv'

# Execute regression for each file name and store results in a list
results_list = []
for file_name in file_names:
    results_summary = execute_regression(file_name)
    results_list.append(results_summary)

# Save the results to a CSV file
header = "Model,R-squared,F-statistic,Coef. MAD,P-value MAD,Coef. Init_gap,P-value Init_gap,Coef. " \
         "Cont_gap,P-value Cont_gap"
with open(output_file, 'w') as f:
    f.write(header + '\n')
    f.write('\n'.join(results_list))

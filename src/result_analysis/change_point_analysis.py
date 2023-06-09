import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt

# Read the Excel file into a DataFrame
current_directory = os.path.join(os.getcwd(), '')
output_directory = current_directory + 'resources/output/latex_tables/lift/'
file = 'cutBajada_4_0_4Bajada_4_0_4_01 (-3).xlsx'

df = pd.read_excel(output_directory + file, sheet_name='cutBajada_4_0_4Bajada_4_0_4_01')

df = df.sort_values('mad_accel(m/s2)')
# df = df.sort_values('mean_length_gaps_mean')
# df = df.sort_values('init_gap')
df = df.sort_values('percentage_matched_snapshots')

# Separate the input variables (X) and the output variable (Y)
X3 = df['mad_accel(m/s2)'].values
X1 = df['init_gap'].values
X2 = df['cont_gap'].values
Y1 = df['percentage_matched_snapshots']
Y2 = df['frechet_euclidean']
Y3 = df['p2p_mean_euclidean_mean']
# Y4 = df['number_of_gaps']
# Y6 = df['mean_length_gaps_mean']


# Combine the input signals and response variable into a signal matrix
signals = np.column_stack((X3, X1, X2, Y1, Y2, Y3))

# Perform change point detection
model = "l2"  # Select the model for change point detection (e.g., "l2", "rbf")
algo = rpt.Dynp(model=model, min_size=3, jump=5)
result = algo.fit_predict(signals, 1)
print(result)

# Plot the data and change point detection results
_, axs = rpt.display(signals, result)

axs[0].set_ylabel('MAD accel(m/s2)')
axs[1].set_ylabel('Init gap')
axs[2].set_ylabel('Cont gap')
axs[3].set_ylabel('%matched snapshots')
axs[4].set_ylabel('Frèchet euclidean')
axs[5].set_ylabel('Euclidean mean')
# axs[6].set_ylabel('Number of gaps')
# axs[7].set_ylabel('Mean length of gaps')

plt.tight_layout()
plt.savefig(output_directory + '/output_affine_a.pdf', format='pdf')
plt.show()

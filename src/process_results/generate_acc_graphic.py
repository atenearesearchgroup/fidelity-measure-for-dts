import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


if __name__ == "__main__":
    # Path to output csv files
    resources_path = os.path.join(os.getcwd(), os.pardir)
    input_path = resources_path + "\\resources\\input\\lift\\derived_values\\"
    filename = "bajarSubir1planta1.csv"

    alignment = pd.read_csv(input_path + filename, delimiter=",")

    # Style for the line plot
    sns.set_theme(style="darkgrid")

    # Select columns to plot from csv
    columns_x = ["timestamp(s)"]
    columns_y = ["accel(m/s2)", "speed(m/s)", "position(m)"]
    fig, axs = plt.subplots(len(columns_y), len(columns_x), sharex='all', figsize=(15, 6))

    for x_index, x in enumerate(columns_x):
        for y_index, y in enumerate(columns_y):
            # Plot line plot using dataframe columns
            if len(columns_x) > 1:
                sns.lineplot(ax=axs[y_index, x_index], data=alignment, x=x, y=y)
            else:
                sns.lineplot(ax=axs[y_index], data=alignment, x=x, y=y)

    # Show the graphic
    plt.show()
    plt.close()

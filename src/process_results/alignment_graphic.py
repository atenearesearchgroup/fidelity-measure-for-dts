import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from util.dataframe_util import clean_df
def generate_graphic(alignment: pd.DataFrame,
                     dt_trace: pd.DataFrame,
                     pt_trace: pd.DataFrame,
                     parameter_of_interest: str,
                     timestamp_label: str,
                     output_path: str = None):
    pt_timestamp = "pt-" + timestamp_label
    dt_timestamp = "dt-" + timestamp_label

    pt_param_interest = "pt-" + parameter_of_interest
    dt_param_interest = "dt-" + parameter_of_interest

    # Separate and clean the dataframe for plotting
    selected_pt = clean_df(pt_trace, [timestamp_label, parameter_of_interest])
    selected_dt = clean_df(dt_trace, [timestamp_label, parameter_of_interest])

    # Set a custom figure size
    plt.figure(figsize=(15, 6))
    plt.subplots_adjust(bottom=0.15)

    # Style for the line plot
    sns.set_theme(style="darkgrid")
    sns.set(font_scale=1.90)

    # Plot line plot using dataframe columns
    # ------------ Physical Twin trajectory
    if parameter_of_interest == 'temperature(degrees)':
        # Difference of -3 to provide better visualization
        selected_pt[parameter_of_interest] = selected_pt[parameter_of_interest].apply(lambda x: x - 3)
    sns.lineplot(data=selected_pt.loc[1:], label="PT", x=timestamp_label, y=parameter_of_interest,
                 marker='o')

    # ------------- Digital Twin trajectory
    ax = sns.lineplot(data=selected_dt.loc[1:], label="DT", x=timestamp_label, y=parameter_of_interest,
                      marker='o', alpha=0.5)

    # Plot alignment with matching points
    for i in range(len(alignment["operation"])):
        if alignment["operation"][i] == "Match":
            if parameter_of_interest == "temperature(degrees)":
                ax.plot([float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                        [float(alignment[pt_param_interest][i])-3, float(alignment[dt_param_interest][i])],
                        color='black', ls=':', zorder=0)
            else:
                ax.plot([float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                        [float(alignment[pt_param_interest][i]), float(alignment[dt_param_interest][i])],
                        color='black', ls=':', zorder=0)

    ax.ticklabel_format(style='plain', axis='both')

    ax.set_title("Trace alignment PT against DT")

    # Limit the x-axis size for better visualization
    # ax.set(xlim=(alignment[pt_al_timestamp][0] - 4, alignment[pt_al_timestamp].max()))
    ax.set_xlabel("POSIX Timestamp (seconds)")

    # Limit the y-axis size for better visualization
    # min = alignment[pt_al_distance].to_numpy()
    # ax.set(ylim=(np.amin(min[min > 0]) - 2, alignment[pt_al_distance].max() + 2))
    ax.set_ylabel(parameter_of_interest)

    ax.legend()

    # Show the graphic
    if output_path is None:
        plt.show()
    else:
        plt.savefig(output_path.replace(".csv", ".pdf"))

    plt.close()

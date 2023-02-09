import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generate_gap_info_graphic(path: str = None):
    # Uncomment to call from Java
    alignment = pd.read_csv(path)

    # Set a custom figure size
    plt.figure(figsize=(15, 6))
    plt.subplots_adjust(bottom=0.15)

    # Style for the line plot
    sns.set_theme(style="darkgrid")
    sns.set(font_scale=1.90)

    fig, axs = plt.subplots(2, 1, sharex='all', figsize=(15, 6))

    # Plot line plot using dataframe columns
    ax = sns.lineplot(ax=axs[0], data=alignment, label="PT", x="gap", y="%matched", marker='o')
    sns.lineplot(ax=axs[1], data=alignment, label="PT", x="gap", y="frechet", marker='o', alpha=0.5)

    ax.ticklabel_format(style='plain', axis='both')

    # Limit the x-axis size for better visualization
    ax.set_title("Alignment result")
    # ax.set(xlim=(alignment[pt_al_timestamp][0] - 4, alignment[pt_al_timestamp].max()))
    ax.set_xlabel("Gap")

    # Limit the y-axis size for better visualization
    # min = alignment[pt_al_distance].to_numpy()
    # ax.set(ylim=(np.amin(min[min > 0]) - 2, alignment[pt_al_distance].max() + 2))
    ax.set_ylabel("% matched points")

    # ax.legend()

    # Show the graphic
    if path is None:
        plt.show()
    else:
        plt.savefig(path.replace(".csv", ".pdf"))

    plt.close()

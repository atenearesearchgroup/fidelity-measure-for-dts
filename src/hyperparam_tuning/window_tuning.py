import logging
import os
import webbrowser

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import ruptures as rpt
from _plotly_utils.colors import sample_colorscale
from plotly.subplots import make_subplots

from hyperparam_tuning import get_change_point
from hyperparam_tuning.window.change_point.factory import ChangePointFactory
from hyperparam_tuning.window.stat_analysis.factory import StatAnalysisFactory
from hyperparam_tuning.window.stat_filters.factory import StatFiltersFactory
from util import list_directory_files


def _get_output_resources_dir():
    path_src = os.path.abspath(os.path.join(os.getcwd(), '../'))
    return os.path.join(path_src, 'resources', 'output')


def _get_relative_filepath(path_list):
    return os.path.join(_get_output_resources_dir(), *path_list)


def calculate_hparams_stats(f_extension, f_starting_pattern, filepath):
    result = pd.DataFrame()
    hyper_analysis = None
    for filename in list_directory_files(filepath, f_extension, f_starting_pattern):
        hyper_analysis = StatAnalysisFactory().get_stat_analysis(filepath, filename)
        result = hyper_analysis.calculate_statistics(filename, result)

    result = result.fillna(-1)
    result.to_csv(os.path.join(filepath, 'results.csv'),
                  index=False)
    return result, hyper_analysis.modifier


def main():
    logging.basicConfig(level=logging.INFO)

    anomaly = [
        'lift',
        'window',
        'NDW_Affine-LCA_Bajada_4_0_4_01_sync'
        'Bajada_4_0_4_01-accel(ms2)'
        '-remove-even'
    ]
    delay = [
        'incubator',
        'window',
        'delay-25',
        'NDW_Affine-4P_exp2_ht20_hg30_Model'
        'exp2_ht20_hg30_Real-temp'
        # 'delay-perfect-figs2',
        # 'NDW_Affine-exp2_ht20_hg30_Realexp2_ht20_hg30_Real-temp'
    ]

    f_starting_pattern = 'du'
    f_extension = '.csv'

    filepath = _get_relative_filepath(delay)

    # hyperparams_stats, modifier = calculate_hparams_stats(f_extension, f_starting_pattern, filepath)
    hyperparams_stats, modifier = pd.read_csv(os.path.join(filepath, 'results.csv')), 'delay'
    hp_filter = StatFiltersFactory.get_filters(modifier, hyperparams_stats)

    filters = [
        hp_filter.filter_period_equals_duration,
        hp_filter.filter_period_less_duration,
        hp_filter.filter_period_greater_duration
    ]

    selected_params = [
        [(0, 15)],
        [(0, 15)],
        [(0, 15)],
    ]

    order_by = [
        [1, 0, 4],
        [1, 0, 4],
        [1, 0, 4],
        # [4, 2, 0, 1]
    ]

    start, stop, n = 0.3, 1, 2
    colors = sample_colorscale('Sunset', np.arange(start, stop, (stop - start) / n))
    markers = ['circle', 'star-square']

    for i, stat_filter in enumerate(filters):
        hp_filter.stats_df = pd.read_csv(os.path.join(filepath, 'results.csv'))
        change_point_info = ChangePointFactory.get_change_point(modifier,
                                                                selected_params[i],
                                                                order_by[i],
                                                                stat_filter)
        filtered_stats = hp_filter.apply_filters(change_point_info.stat_filter)
        filtered_stats = filtered_stats.sort_values(by=change_point_info.order_by)

        # change_point(change_point_info, filtered_stats)
        fig = make_subplots(rows=6, cols=1, shared_xaxes=True)
        fig.update_layout(template='plotly')
        groups = [1, 1, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        for j, p in enumerate(change_point_info.params):
            fig.add_trace(go.Scatter(x=np.arange(filtered_stats.shape[0]), y=filtered_stats[p],
                                     name=p,
                                     mode='lines',
                                     line=dict(
                                         color=colors[j % n],
                                         width=1
                                     ),
                                     marker=dict(
                                         # size=4,
                                         color=colors[j % n],
                                         symbol=markers[j % n]
                                     )),
                          row=groups[j], col=1)
            if j > 3:
                fig['layout'][f"yaxis{groups[j] if j > 0 else ''}"]['title'] = p[:-6]
                # fig['layout'][f"yaxis{groups[i] if i > 0 else ''}"]['range'] = [-5, 105]
            else:
                fig['layout'][f"yaxis{groups[j] if j > 0 else ''}"]['title'] = p

        fig['layout'][f'xaxis{6}']['title'] = '#WindowAlignments'

        # Save the plot as an HTML file
        pio.write_html(fig, f'plotly_figure{i}.html')
        #
        # # Open the HTML file in the default web browser
        webbrowser.open(f'plotly_figure{i}.html')

        # formula = 'min_per_ms ~ (du-an_len)/du'
        # model = smf.ols(formula=formula, data=filtered_result).fit()
        #
        # # Print the summary of the regression
        # print(model.summary())


def change_point(change_point_info, filtered_stats):
    signals, result = get_change_point(filtered_stats,
                                       change_point_info.order_by,
                                       change_point_info.params,
                                       number_of_changes=1)
    _, axs = rpt.display(signals, result)
    # axs[len(change_point_info.params) - 5].plot(np.arange(len(filtered_stats)),
    #                                             signals[:, 7])
    # axs[len(change_point_info.params) - 3].plot(np.arange(len(filtered_stats)),
    #                                   signals[:, 8])
    for i, label in enumerate(change_point_info.params):
        axs[i].set_ylabel(label)
        if i > 2 and i not in [5, 8, 11, 12, 13, 14]:
            axs[i].set_ylim(-5, 105)
    axs[len(change_point_info.params) - 1].set_xlabel('#Windows')
    plt.tight_layout()
    plt.show()
    print('hi')


if __name__ == "__main__":
    main()

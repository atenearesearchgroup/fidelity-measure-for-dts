import numpy as np
import pandas as pd
import plotly.graph_objects as go
from _plotly_utils.colors import sample_colorscale
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

import util.file_util as fu

# RELEVANT STRINGS
MAD = 'mad_'
MATCHED_SNAPSHOTS_LCA = 'percentage_matched_snapshots_lca'
FRECHET_LCA = 'frechet_lca_euclidean'
P2P_EUCLIDEAN_LCA = 'p2p_mean_lca_euclidean_mean'

MATCHED_SNAPSHOTS = 'percentage_matched_snapshots'
FRECHET = 'frechet_euclidean'
P2P_EUCLIDEAN = 'p2p_mean_euclidean_mean'

# AXIS STRING CONSTANTS
MATCHED_SNAPSHOTS_AXIS = '%MS'
FRECHET_AXIS = 'FD'
P2P_EUCLIDEAN_AXIS = 'ED'
MAD_AXIS = 'MAD'

# FONT OPTIONS
FONT_SIZE = 24


def generate_parallel_behavior_graphic(x_axis_var: str,
                                       x_axis_title: str,
                                       y_axis_var: str,
                                       y_axis_title: str,
                                       traces_paths: list,
                                       traces_labels: list):
    """
    Generates two graphics sharing the x-axis with the trajectories of the PT and DT
    :param traces_labels:
    :param traces_paths:
    :param y_axis_title:
    :param x_axis_title:
    :param x_axis_var: variable to set in x_axis
    :param y_axis_var: variable to set in y_axis
    :return:
    """
    colors = sample_colorscale('Sunset', [0.70, 0.20])
    fig = make_subplots(rows=len(traces_labels),
                        cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    for index, label in enumerate(traces_labels):
        trace_a_alignment = pd.read_csv(traces_paths[index])
        fig.add_trace(go.Scatter(x=trace_a_alignment[x_axis_var], y=trace_a_alignment[y_axis_var],
                                 mode='lines+markers',
                                 name=label,
                                 marker=dict(
                                     size=6,
                                     color=colors[index]
                                 ),
                                 line=dict(
                                     width=2,
                                     color=colors[index]
                                 )),
                      row=(index + 1), col=1)
        fig['layout'][f'yaxis{index + 1}']['title'] = y_axis_title

    fig['layout'][f'xaxis{len(traces_labels)}']['title'] = x_axis_title

    # Distance between titles and axes to 0
    fig.update_yaxes(showline=True, linewidth=1, linecolor='gray', tickprefix=" ", ticksuffix=" ",
                     title_standoff=4)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', tickprefix=" ", ticksuffix=" ",
                     title_standoff=4)

    fig.update_layout(
        template='plotly_white',
        font=dict(
            size=FONT_SIZE
        ),  # Figure font
        legend=dict(  # Legend position
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(t=0, l=0, r=0, b=0)
    )

    return fig


def generate_statistical_info_stairs_comparison(x_axis_var: str,
                                                trace_a_path: str,
                                                trace_a_label: str,
                                                trace_b_path: str,
                                                trace_b_label: str,
                                                x_axis_upper_bound: float = None,
                                                x_axis_lower_bound: float = None,
                                                range_ms: list = None,
                                                range_fd: list = None,
                                                range_ed: list = None,
                                                units: str = '',
                                                lca: bool = False):
    """
    Generates scatter plot comparing the statistical values of %matches points, frechet and euclidean distance of
    two alignments
    :param units:
    :param range_ed:
    :param range_fd:
    :param range_ms:
    :param trace_a_label:
    :param trace_b_label:
    :param x_axis_upper_bound:
    :param x_axis_lower_bound:
    :param x_axis_var:
    :param trace_a_path:
    :param trace_b_path:
    :return:
    """
    colors = sample_colorscale('Sunset', [0.24, 0.90])
    markers = ['circle', 'star-square']

    # Get dataframe from csv file
    trace_a_alignment = pd.read_csv(trace_a_path, index_col=False)
    trace_b_alignment = pd.read_csv(trace_b_path, index_col=False)

    # Use LCA statistics
    if lca:
        matched_snapshots = MATCHED_SNAPSHOTS_LCA
        frechet = FRECHET_LCA
        p2p_euclidean = P2P_EUCLIDEAN_LCA
    else:
        matched_snapshots = MATCHED_SNAPSHOTS
        frechet = FRECHET
        p2p_euclidean = P2P_EUCLIDEAN

    # Filter desired range
    if x_axis_lower_bound:
        trace_a_alignment = trace_a_alignment[trace_a_alignment[x_axis_var] > x_axis_lower_bound]
        trace_b_alignment = trace_b_alignment[trace_b_alignment[x_axis_var] > x_axis_lower_bound]
    if x_axis_upper_bound:
        trace_a_alignment = trace_a_alignment[trace_a_alignment[x_axis_var] < x_axis_upper_bound]
        trace_b_alignment = trace_b_alignment[trace_b_alignment[x_axis_var] < x_axis_upper_bound]

    # Create traces
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05)
    fig.update_layout(template='plotly')

    fig.add_trace(
        go.Scatter(x=trace_a_alignment[x_axis_var], y=trace_a_alignment[matched_snapshots],
                   mode='lines+markers',
                   name=trace_a_label,
                   line=dict(color=colors[0]),
                   marker=dict(color=colors[0],
                               symbol=markers[0],
                               size=10)
                   ),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=trace_b_alignment[x_axis_var], y=trace_b_alignment[matched_snapshots],
                   mode='lines+markers',
                   name=trace_b_label,
                   line=dict(color=colors[1]),
                   marker=dict(color=colors[1],
                               symbol=markers[1],
                               size=10),
                   fill='tonexty'
                   ),
        row=1, col=1)

    fig['layout']['yaxis']['title'] = MATCHED_SNAPSHOTS_AXIS
    if range_ms is not None:
        fig['layout']['yaxis']['range'] = range_ms

    fig.add_trace(go.Scatter(x=trace_a_alignment[x_axis_var], y=trace_a_alignment[frechet],
                             mode='lines+markers',
                             line=dict(color=colors[0]),
                             marker=dict(color=colors[0],
                                         symbol=markers[0],
                                         size=10),
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=trace_b_alignment[x_axis_var], y=trace_b_alignment[frechet],
                             mode='lines+markers',
                             line=dict(color=colors[1]),
                             marker=dict(color=colors[1],
                                         symbol=markers[1],
                                         size=10),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = f'{FRECHET_AXIS} {units}'
    if range_fd is not None:
        fig['layout']['yaxis2']['range'] = range_fd

    fig.add_trace(go.Scatter(x=trace_a_alignment[x_axis_var], y=trace_a_alignment[p2p_euclidean],
                             mode='lines+markers',
                             line=dict(color=colors[0]),
                             marker=dict(color=colors[0],
                                         symbol=markers[0],
                                         size=10),
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=trace_b_alignment[x_axis_var], y=trace_b_alignment[p2p_euclidean],
                             mode='lines+markers',
                             line=dict(color=colors[1]),
                             marker=dict(color=colors[1],
                                         symbol=markers[1],
                                         size=10),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = f'{P2P_EUCLIDEAN_AXIS} {units}'
    if range_ed is not None:
        fig['layout']['yaxis3']['range'] = range_ed

    fig['layout']['xaxis3']['title'] = f'{MAD_AXIS} {units}'

    fig.update_yaxes(showline=True, linewidth=1, linecolor='gray', tickprefix=" ", ticksuffix=" ",
                     title_standoff=4)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', tickprefix=" ", ticksuffix=" ",
                     title_standoff=10)

    fig.update_layout(
        template='plotly_white',
        font=dict(
            size=FONT_SIZE
        ),  # Figure font
        legend=dict(  # Legend position
            yanchor="top",
            y=0.88,
            xanchor="right",
            x=0.95
        ),
        margin=dict(t=0, l=0, r=0, b=0)
    )

    return fig


def generate_statistical_info_stairs(x_axis_var: str,
                                     alignment_df: pd.DataFrame,
                                     units: str,
                                     fig: Figure = make_subplots(rows=3, cols=1, shared_xaxes=True,
                                                                 vertical_spacing=0.0),
                                     range_ms: list = None,
                                     range_fd: list = None,
                                     range_ed: list = None,
                                     lca: bool = False):
    """
    Generates a scatter plot with the %of matched points, the frechet and the Euclidean distance for
    a given alignment
    :param range_ed:
    :param range_fd:
    :param range_ms:
    :param units:
    :param lca:
    :param alignment_df:
    :param fig:
    :param x_axis_var:
    :return:
    """
    fig.update_layout(template='plotly')

    # Use LCA statistics
    if lca:
        matched_snapshots = MATCHED_SNAPSHOTS_LCA
        frechet = FRECHET_LCA
        p2p_euclidean = P2P_EUCLIDEAN_LCA
    else:
        matched_snapshots = MATCHED_SNAPSHOTS
        frechet = FRECHET
        p2p_euclidean = P2P_EUCLIDEAN

    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[matched_snapshots],
                             mode='lines',
                             line=dict(
                                 color='#898989',
                                 width=0.5),
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = MATCHED_SNAPSHOTS_AXIS
    if range_ms is not None:
        fig['layout']['yaxis']['range'] = range

    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[frechet],
                             mode='lines',
                             showlegend=False,
                             line=dict(color='#898989',
                                       width=0.5),
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = f'{FRECHET_AXIS} {units}'
    if range_fd is not None:
        fig['layout']['yaxis2']['range'] = range_fd

    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[p2p_euclidean],
                             mode='lines',
                             showlegend=False,
                             line=dict(color='#898989',
                                       width=0.5),
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = f'{P2P_EUCLIDEAN_AXIS} {units}'
    fig['layout']['xaxis3']['title'] = f'{MAD_AXIS} {units}'

    if range_ed is not None:
        fig['layout']['yaxis3']['range'] = range_ed

    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    fig.update_layout(
        font=dict(
            # size=FONT_SIZE
        ),
        showlegend=False,
        margin=dict(t=0, l=0, r=0, b=0)
    )
    return fig


def generate_statistical_info_stairs_variability(x_axis_var: str,
                                                 path: str,
                                                 starting_pattern: str,
                                                 units: str,
                                                 range_ms: list = None,
                                                 range_fd: list = None,
                                                 range_ed: list = None,
                                                 lca: bool = False,
                                                 x_axis_upper_bound: float = None,
                                                 x_axis_lower_bound: float = None
                                                 ):
    # Use LCA statistics
    if lca:
        matched_snapshots = MATCHED_SNAPSHOTS_LCA
        frechet = FRECHET_LCA
        p2p_euclidean = P2P_EUCLIDEAN_LCA
    else:
        matched_snapshots = MATCHED_SNAPSHOTS
        frechet = FRECHET
        p2p_euclidean = P2P_EUCLIDEAN

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    fig.update_layout(template='plotly')

    variability_df = pd.DataFrame(columns=[x_axis_var, matched_snapshots, frechet, p2p_euclidean])

    for align_file in fu.list_directory_files(path, ".csv", starting_pattern):
        alignment = pd.read_csv(path + "/" + align_file, index_col=False)

        # Filter desired range
        if x_axis_lower_bound:
            alignment = alignment[alignment[x_axis_var] > x_axis_lower_bound]
        if x_axis_upper_bound:
            alignment = alignment[alignment[x_axis_var] < x_axis_upper_bound]

        for _, row in alignment.iterrows():
            new_row = {x_axis_var: row[x_axis_var].round(2),
                       matched_snapshots: row[matched_snapshots],
                       frechet: row[frechet],
                       p2p_euclidean: row[p2p_euclidean]}
            variability_df = pd.concat([variability_df, pd.DataFrame([new_row])], ignore_index=True)

    rows = variability_df.drop_duplicates([x_axis_var])[x_axis_var]
    result_df = pd.DataFrame()
    table_df = pd.DataFrame()
    for row in rows:
        average = np.mean(variability_df.loc[variability_df[x_axis_var] == row], axis=0)
        std = np.std(variability_df.loc[variability_df[x_axis_var] == row], axis=0)
        new_row = {x_axis_var: row,
                   f'{matched_snapshots}_avg': average[matched_snapshots],
                   f'{matched_snapshots}_std': std[matched_snapshots],
                   f'{frechet}_avg': average[frechet],
                   f'{frechet}_std': std[frechet],
                   f'{p2p_euclidean}_avg': average[p2p_euclidean],
                   f'{p2p_euclidean}_std': std[p2p_euclidean]}
        new_table_row = {x_axis_var: row,
                         MATCHED_SNAPSHOTS_AXIS: f'{average[matched_snapshots]:.4f} ± {std[matched_snapshots]:.4f}',
                         FRECHET_AXIS: f'{average[frechet]:.4f} ± {std[frechet]:.4f}',
                         P2P_EUCLIDEAN_AXIS: f'{average[p2p_euclidean]:.4f} ± {std[p2p_euclidean]:.4f}'}
        result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)
        table_df = pd.concat([table_df, pd.DataFrame([new_table_row])], ignore_index=True)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{matched_snapshots}_avg'],
                             mode='lines+markers',
                             ),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{matched_snapshots}_avg'] + result_df[
                                 f'{matched_snapshots}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             name='upper bound'))

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{matched_snapshots}_avg'] - result_df[
                                 f'{matched_snapshots}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             fill='tonexty',
                             name='lower bound'))

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{frechet}_avg'],
                             mode='lines+markers',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{frechet}_avg'] + result_df[f'{frechet}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             name='upper bound'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{frechet}_avg'] - result_df[f'{frechet}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             fill='tonexty',
                             name='lower bound'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{p2p_euclidean}_avg'],
                             mode='lines+markers',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(
        go.Scatter(x=result_df[x_axis_var],
                   y=result_df[f'{p2p_euclidean}_avg'] + result_df[f'{p2p_euclidean}_std'],
                   mode='lines',
                   line=dict(width=0.1),
                   name='upper bound'),
        row=3, col=1)

    fig.add_trace(
        go.Scatter(x=result_df[x_axis_var],
                   y=result_df[f'{p2p_euclidean}_avg'] - result_df[f'{p2p_euclidean}_std'],
                   mode='lines',
                   line=dict(width=0.1),
                   fill='tonexty',
                   name='lower bound'),
        row=3, col=1)

    for align_file in fu.list_directory_files(path, ".csv", starting_pattern):
        alignment = pd.read_csv(path + "/" + align_file, index_col=False)
        # Filter desired range
        if x_axis_lower_bound:
            alignment = alignment[alignment[x_axis_var] > x_axis_lower_bound]
        if x_axis_upper_bound:
            alignment = alignment[alignment[x_axis_var] < x_axis_upper_bound]
        generate_statistical_info_stairs(x_axis_var, alignment, units, fig, lca=lca)

    if range_ms is not None:
        fig['layout']['yaxis']['range'] = range_ms

    if range_fd is not None:
        fig['layout']['yaxis2']['range'] = range_fd

    if range_ed is not None:
        fig['layout']['yaxis3']['range'] = range_ed

    fig.update_layout(
        font=dict(
            # size=FONT_SIZE
        ),
        margin=dict(t=0, l=0, r=0, b=0)
    )
    fig.update_yaxes(tickprefix="  ", ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=10)

    return fig, table_df

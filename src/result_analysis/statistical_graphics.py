import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

import util.file_util as fu

# RELEVANT STRINGS
MAD = 'mad_'
MATCHED_SNAPSHOTS = 'percentage_matched_snapshots'
FRECHET = 'frechet_euclidean'
P2P_EUCLIDEAN = 'p2p_mean_lca_euclidean_mean'


def generate_parallel_behavior_graphic(x_axis_var: str, x_axis_title: str, y_axis_var: str, y_axis_title: str,
                                       pt_path: str,
                                       dt_path: str,
                                       t_path: str):
    """
    Generates two graphics sharing the x-axis with the trajectories of the PT and DT
    :param y_axis_title:
    :param x_axis_title:
    :param x_axis_var: variable to set in x_axis
    :param y_axis_var: variable to set in y_axis
    :param pt_path:
    :param dt_path:
    :return:
    """
    # Create subplots
    fig = make_subplots(rows=3,
                        cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    ### PHYSICAL TWIN ###
    # Get PT dataframe from csv file
    alignment = pd.read_csv(pt_path)
    # Plot PT trace
    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment[y_axis_var],
                             mode='lines+markers',
                             name='PT Trajectory',
                             marker=dict(
                                 size=6,
                                 line_width=0
                             ),
                             line=dict(
                                 width=2
                             )),
                  row=1, col=1)
    fig['layout']['yaxis']['title'] = y_axis_title

    ### DIGITAL TWIN ###
    # Get DT dataframe from csv file
    alignment = pd.read_csv(dt_path)
    # Plot DT trace
    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment[y_axis_var],
                             mode='lines+markers',
                             name='2-parameter model trajectory',
                             marker=dict(
                                 size=6,
                                 line_width=0
                             ),
                             line=dict(
                                 width=2
                             )),
                  row=2, col=1)
    fig['layout']['yaxis2']['title'] = y_axis_title
    # fig['layout']['xaxis2']['title'] = x_axis_title

    ### DIGITAL TWIN ###
    # Get DT dataframe from csv file
    alignment = pd.read_csv(t_path)
    # Plot DT trace
    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment[y_axis_var],
                             mode='lines+markers',
                             name='4-parameter model trajectory',
                             marker=dict(
                                 size=6,
                                 line_width=0
                             ),
                             line=dict(
                                 width=2
                             )),
                  row=3, col=1)
    fig['layout']['yaxis3']['title'] = y_axis_title
    fig['layout']['xaxis3']['title'] = x_axis_title

    # Distance between titles and axes to 0
    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)

    fig.update_layout(
        # xaxis_range=[0, 64],  # x axis range
        font=dict(
            size=12),  # Figure font
        legend=dict(  # Legend position
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

    # Show figure
    fig.show()
    return fig


def generate_statistical_info_stairs_comparison(x_axis_var: str, high_fid_path: str, low_fid_path: str):
    """
    Generates scatter plot comparing the statistical values of %matches points, frechet and euclidean distance of
    two alignments
    :param x_axis_var:
    :param high_fid_path:
    :param low_fid_path:
    :return:
    """
    # Get dataframe from csv file
    high_fid_align = pd.read_csv(high_fid_path, index_col=False)
    low_fid_aling = pd.read_csv(low_fid_path, index_col=False)

    # Create traces
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.0)

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[MATCHED_SNAPSHOTS],
                             mode='lines+markers',
                             name='High-fidelity',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E')
                             ),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[MATCHED_SNAPSHOTS],
                             mode='lines+markers',
                             name='Low-fidelity',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty'
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = "%matched snapshots"
    fig['layout']['yaxis']['range'] = [0, 100]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[FRECHET],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[FRECHET],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = "Fréchet (m/s2)"
    fig['layout']['yaxis2']['range'] = [0, 0.2]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[P2P_EUCLIDEAN],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[P2P_EUCLIDEAN],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = "Eucl. avg (m/s2)"
    fig['layout']['xaxis3']['title'] = "Maximum acceptable distance (m/s2)"
    fig['layout']['yaxis3']['range'] = [0, 0.03]

    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    # fig.update_layout(showlegend=False)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.show()
    # fig.write_html(path.replace(".csv", "") + "_" + x_axis_var + ".html")


def generate_statistical_info_stairs_comparison_lca(x_axis_var: str, high_fid_path: str, low_fid_path: str):
    """
    Generates scatter plot comparing the statistical values of %matches points, frechet and euclidean distance of
    two alignments
    :param x_axis_var:
    :param high_fid_path:
    :param low_fid_path:
    :return:
    """
    # Get dataframe from csv file
    high_fid_align = pd.read_csv(high_fid_path, index_col=False)
    low_fid_aling = pd.read_csv(low_fid_path, index_col=False)

    # Create traces
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.0)

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[MATCHED_SNAPSHOTS],
                             mode='lines+markers',
                             name='High-fidelity',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E')
                             ),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[MATCHED_SNAPSHOTS],
                             mode='lines+markers',
                             name='Low-fidelity',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty'
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = "%matched points"
    fig['layout']['yaxis']['range'] = [0, 100]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[FRECHET],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[FRECHET],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = "Fréchet (m/s2)"
    fig['layout']['yaxis2']['range'] = [0, 0.2]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align[P2P_EUCLIDEAN],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling[P2P_EUCLIDEAN],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = "Eucl. Avg. (m/s2)"
    fig['layout']['xaxis3']['title'] = "Maximum acceptable distance (m/s2)"
    fig['layout']['yaxis3']['range'] = [0, 0.03]

    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    # fig.update_layout(showlegend=False)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.show()
    # fig.write_html(path.replace(".csv", "") + "_" + x_axis_var + ".html")


def generate_statistical_info_stairs(x_axis_var: str, alignment_df: pd.DataFrame,
                                     fig: Figure = make_subplots(rows=3, cols=1, shared_xaxes=True,
                                                                 vertical_spacing=0.0), fig_show=False):
    """
    Generates a scatter plot with the %of matched points, the frechet and the Euclidean distance for
    a given alignment
    :param fig_show:
    :param alignment_df:
    :param fig:
    :param x_axis_var:
    :param path:
    :return:
    """
    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[MATCHED_SNAPSHOTS],
                             mode='lines',
                             line=dict(
                                 color='#898989',
                                 width=0.5),
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = "%matched points"
    fig['layout']['yaxis']['range'] = [0, 100]

    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[FRECHET],
                             mode='lines',
                             showlegend=False,
                             line=dict(color='#898989',
                                       width=0.5),
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = "Fréchet (m/s2)"
    fig['layout']['yaxis2']['range'] = [0, 0.3]

    fig.add_trace(go.Scatter(x=alignment_df[x_axis_var], y=alignment_df[P2P_EUCLIDEAN],
                             mode='lines',
                             showlegend=False,
                             line=dict(color='#898989',
                                       width=0.5),
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = "Eucl. Avg. (m/s2)"
    fig['layout']['xaxis3']['title'] = "Maximum acceptable distance (m/s2)"
    fig['layout']['yaxis3']['range'] = [0, 0.03]

    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    fig.update_layout(showlegend=False)

    if fig_show:
        fig.show()
    # fig.write_html(path.replace(".csv", "") + "_" + x_axis_var + ".html")


def generate_statistical_info_stairs_variability(x_axis_var: str, path: str, starting_pattern: str):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    variability_df = pd.DataFrame(columns=[x_axis_var, MATCHED_SNAPSHOTS, FRECHET, P2P_EUCLIDEAN])
    for align_file in fu.list_directory_files(path, ".csv", starting_pattern):
        alignment = pd.read_csv(path + "/" + align_file, index_col=False)

        # Add data to the plot
        # generate_statistical_info_stairs(x_axis_var, alignment, fig)

        for _, row in alignment.iterrows():
            new_row = {x_axis_var: row[x_axis_var].round(2),
                       MATCHED_SNAPSHOTS: row[MATCHED_SNAPSHOTS],
                       FRECHET: row[FRECHET],
                       P2P_EUCLIDEAN: row[P2P_EUCLIDEAN]}
            variability_df = pd.concat([variability_df, pd.DataFrame([new_row])], ignore_index=True)

    rows = variability_df.drop_duplicates([x_axis_var])[x_axis_var]
    result_df = pd.DataFrame()
    table_df = pd.DataFrame()
    for row in rows:
        average = np.mean(variability_df.loc[variability_df[x_axis_var] == row], axis=0)
        std = np.std(variability_df.loc[variability_df[x_axis_var] == row], axis=0)
        new_row = {x_axis_var: row,
                   f'{MATCHED_SNAPSHOTS}_avg': average[MATCHED_SNAPSHOTS],
                   f'{MATCHED_SNAPSHOTS}_std': std[MATCHED_SNAPSHOTS],
                   f'{FRECHET}_avg': average[FRECHET],
                   f'{FRECHET}_std': std[FRECHET],
                   f'{P2P_EUCLIDEAN}_avg': average[P2P_EUCLIDEAN],
                   f'{P2P_EUCLIDEAN}_std': std[P2P_EUCLIDEAN]}
        new_table_row = {x_axis_var: row,
                         '% matched': f'{average[MATCHED_SNAPSHOTS]:.4f} ± {std[MATCHED_SNAPSHOTS]:.4f}',
                         'Frèchet': f'{average[FRECHET]:.4f} ± {std[FRECHET]:.4f}',
                         'Avg. Euclidean': f'{average[P2P_EUCLIDEAN]:.4f} ± {std[P2P_EUCLIDEAN]:.4f}'}
        result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)
        table_df = pd.concat([table_df, pd.DataFrame([new_table_row])], ignore_index=True)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{MATCHED_SNAPSHOTS}_avg'],
                             mode='lines+markers',
                             ),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{MATCHED_SNAPSHOTS}_avg'] + result_df[f'{MATCHED_SNAPSHOTS}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             name='upper bound'))

    fig.add_trace(go.Scatter(x=result_df[x_axis_var],
                             y=result_df[f'{MATCHED_SNAPSHOTS}_avg'] - result_df[f'{MATCHED_SNAPSHOTS}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             fill='tonexty',
                             name='lower bound'))

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{FRECHET}_avg'],
                             mode='lines+markers',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{FRECHET}_avg'] + result_df[f'{FRECHET}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             name='upper bound'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{FRECHET}_avg'] - result_df[f'{FRECHET}_std'],
                             mode='lines',
                             line=dict(width=0.1),
                             fill='tonexty',
                             name='lower bound'),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=result_df[x_axis_var], y=result_df[f'{P2P_EUCLIDEAN}_avg'],
                             mode='lines+markers',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(
        go.Scatter(x=result_df[x_axis_var], y=result_df[f'{P2P_EUCLIDEAN}_avg'] + result_df[f'{P2P_EUCLIDEAN}_std'],
                   mode='lines',
                   line=dict(width=0.1),
                   name='upper bound'),
        row=3, col=1)

    fig.add_trace(
        go.Scatter(x=result_df[x_axis_var], y=result_df[f'{P2P_EUCLIDEAN}_avg'] - result_df[f'{P2P_EUCLIDEAN}_std'],
                   mode='lines',
                   line=dict(width=0.1),
                   fill='tonexty',
                   name='lower bound'),
        row=3, col=1)

    for align_file in fu.list_directory_files(path, ".csv", starting_pattern):
        alignment = pd.read_csv(path + "/" + align_file, index_col=False)
        generate_statistical_info_stairs(x_axis_var, alignment, fig)

    fig['layout']['yaxis']['range'] = [0, 100]
    fig['layout']['yaxis2']['range'] = [0, 0.20]
    fig['layout']['yaxis3']['range'] = [0, 0.07]
    fig.update_layout()

    fig.show()
    # Save the DataFrame to a CSV file
    output_file = f'{path}/results/variability_results_{starting_pattern}.csv'
    table_df.to_csv(output_file, index=False)
    return fig

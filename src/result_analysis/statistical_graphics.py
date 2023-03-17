import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_paralell_behavior_graphic(x_axis_var: str, x_axis_title: str, y_axis_var: str, y_axis_title: str, pt_path: str,
                      dt_path: str):
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
    fig = make_subplots(rows=2,
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
                                 size=3,
                                 line_width=0.5
                             ),
                             line=dict(
                                 width=1
                             )),
                  row=1, col=1)
    fig['layout']['yaxis']['title'] = y_axis_title

    ### DIGITAL TWIN ###
    # Get DT dataframe from csv file
    alignment = pd.read_csv(dt_path)
    # Plot DT trace
    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment[y_axis_var],
                             mode='lines+markers',
                             name='DT Trajectory',
                             marker=dict(
                                 size=3,
                                 line_width=0.5
                             ),
                             line=dict(
                                 width=1
                             )),
                  row=2, col=1)
    fig['layout']['yaxis2']['title'] = y_axis_title
    fig['layout']['xaxis2']['title'] = x_axis_title

    # Distance between titles and axes to 0
    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)

    fig.update_layout(
        xaxis_range=[0, 64],  # x axis range
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


def generate_statistical_info_graphic(x_axis_var: str, path: str):
    """
    Generates four scatter plots with shared x of all the statistical information of a trace
    :param x_axis_var:
    :param path:
    :return:
    """
    # Get dataframe from csv file
    alignment = pd.read_csv(path)

    # Create traces
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)

    # Gap length
    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['gap_length_mean'],
                             mode='lines+markers',
                             error_y=dict(
                                 type='data',
                                 symmetric=True,
                                 array=alignment['gap_length_std']
                             ),
                             name='Gap Mean Length'),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['gap_individual'],
                             mode='lines+markers',
                             name='Number of individual gaps'
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['gap_groups'],
                             mode='lines+markers',
                             name='Number of groups of gaps'
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['%matched'],
                             mode='lines+markers',
                             name='% of matched points'
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['%mismatch'],
                             mode='lines+markers',
                             name='% of mismatches'
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['frechet'],
                             mode='lines+markers',
                             name='Frèchet distance'
                             ),
                  row=4, col=1)

    fig.show()
    fig.write_html(path.replace(".csv", "") + "_" + x_axis_var + ".html")


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

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align['%matched'],
                             mode='lines+markers',
                             name='High-fidelity',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E')
                             ),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling['%matched'],
                             mode='lines+markers',
                             name='Low-fidelity',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty'
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = "%matched points"
    fig['layout']['yaxis']['range'] = [0, 100]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align['frechet'],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=2, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling['frechet'],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = "Fréchet (m/s2)"
    fig['layout']['yaxis2']['range'] = [0, 0.5]

    fig.add_trace(go.Scatter(x=high_fid_align[x_axis_var], y=high_fid_align['match_mean'],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=3, col=1)

    fig.add_trace(go.Scatter(x=low_fid_aling[x_axis_var], y=low_fid_aling['match_mean'],
                             mode='lines+markers',
                             line=dict(color='#636EFA'),
                             marker=dict(color='#636EFA'),
                             fill='tonexty',
                             showlegend=False
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = "Eucl. mean (m/s2)"
    fig['layout']['xaxis3']['title'] = "Maximum acceptable distance (m/s2)"
    fig['layout']['yaxis3']['range'] = [0, 0.25]

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


def generate_statistical_info_stairs(x_axis_var: str, path: str):
    """
    Generates a scatter plot with the %of matched points, the frechet and the euclidean distance for
    a given alignment
    :param x_axis_var:
    :param path:
    :return:
    """
    # Get dataframe from csv file
    alignment = pd.read_csv(path, index_col=False)

    # Create traces
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.0)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['%matched'],
                             mode='lines+markers',
                             name='High-fidelity',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E')
                             ),
                  row=1, col=1)

    fig['layout']['yaxis']['title'] = "%matched points"
    fig['layout']['yaxis']['range'] = [0, 100]

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['frechet'],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=2, col=1)

    fig['layout']['yaxis2']['title'] = "Fréchet (m/s2)"
    fig['layout']['yaxis2']['range'] = [0, 0.5]

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['match_mean'],
                             mode='lines+markers',
                             line=dict(color='#FF7F0E'),
                             marker=dict(color='#FF7F0E'),
                             showlegend=False
                             ),
                  row=3, col=1)

    fig['layout']['yaxis3']['title'] = "Eucl. mean (m/s2)"
    fig['layout']['xaxis3']['title'] = "Maximum acceptable distance (m/s2)"
    fig['layout']['yaxis3']['range'] = [0, 0.25]

    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    fig.update_layout(showlegend=False)

    #fig.update_layout(legend=dict(
    #    yanchor="top",
    #    y=0.99,
    #    xanchor="left",
    #    x=0.01
    #))

    fig.show()
    fig.write_html(path.replace(".csv", "") + "_" + x_axis_var + ".html")

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def generate_statistical_info_graphic(x_axis_var: str, path: str):
    # Get dataframe from csv file
    alignment = pd.read_csv(path)

    # Create traces
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True)

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

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['frechet'],
                             mode='lines+markers',
                             name='Frèchet distance'
                             ),
                  row=4, col=1)

    fig.add_trace(go.Scatter(x=alignment[x_axis_var], y=alignment['f-score'],
                             mode='lines+markers',
                             name='F-Score'
                             ),
                  row=5, col=1)

    fig.show()
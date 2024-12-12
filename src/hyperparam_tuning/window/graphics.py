import numpy as np
import plotly.graph_objects as go
from _plotly_utils.colors import sample_colorscale
from plotly.subplots import make_subplots

MATCHED_SNAPSHOTS = 'percentage_matched_snapshots'
PERCENTAGE_GAPS = 'percentage_gaps'
FRECHET = 'frechet_euclidean'
P2P_EUCLIDEAN = 'p2p_mean_euclidean_mean'
FONT_SIZE = 15


def generate_window_statistics(dt_trace, pt_trace, alignment_stats_df, param_interest,
                               timestamp_label, mad):
    max_value = max(alignment_stats_df[FRECHET].max(), mad)

    window_ts = dt_trace.loc[alignment_stats_df['w_end']][timestamp_label]
    plots = {f'DT {param_interest}': (dt_trace[timestamp_label], dt_trace[param_interest], []),
             f'PT {param_interest}': (pt_trace[timestamp_label], pt_trace[param_interest], []),
             '% MS': (window_ts, alignment_stats_df[MATCHED_SNAPSHOTS], [0, 100]),
             '% gaps': (window_ts, alignment_stats_df[PERCENTAGE_GAPS], [0, 100]),
             'FD': (window_ts, alignment_stats_df[FRECHET], [0, max_value]),
             'ED': (window_ts, alignment_stats_df[P2P_EUCLIDEAN], [0, max_value])}

    start, stop, n = 0.3, 1, len(plots)
    colors = sample_colorscale('Sunset', np.arange(start, stop, (stop - start) / n))

    fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                        vertical_spacing=0.02)
    fig.update_layout(template='plotly')

    for i, (k, v) in enumerate(plots.items(), 1):
        fig.add_trace(go.Scatter(x=v[0], y=v[1],
                                 mode='lines+markers',
                                 line=dict(
                                     color=colors[i - 1],
                                     width=1
                                 ),
                                 marker=dict(
                                     size=2,
                                     color=colors[i - 1],
                                 ),
                                 ),
                      row=i, col=1)

        fig['layout'][f"yaxis{i if i > 0 else ''}"]['title'] = k
        if v[2]:
            fig['layout'][f"yaxis{i if i > 0 else ''}"]['range'] = v[2]

    fig['layout'][f'xaxis{n}']['title'] = timestamp_label
    fig.update_yaxes(ticksuffix=" ", title_standoff=2)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)
    fig.update_layout(
        # template='plotly_white',
        font=dict(
            size=FONT_SIZE
        ),
        showlegend=False,
        margin=dict(t=0, l=0, r=0, b=0)
    )
    return fig

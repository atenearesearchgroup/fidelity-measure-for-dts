import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots

from util.dataframe_util import clean_df


def generate_alignment_graphic(alignment: pd.DataFrame,
                               dt_trace: pd.DataFrame,
                               pt_trace: pd.DataFrame,
                               parameter_of_interest: str,
                               timestamp_label: str,
                               tolerance: float,
                               open_gap: float,
                               continue_gap: float,
                               output_path: str = None):
    pt_timestamp = "pt-" + timestamp_label
    dt_timestamp = "dt-" + timestamp_label

    pt_param_interest = "pt-" + parameter_of_interest
    dt_param_interest = "dt-" + parameter_of_interest

    # Separate and clean the dataframe for plotting
    selected_pt = clean_df(pt_trace, [timestamp_label, parameter_of_interest])
    selected_dt = clean_df(dt_trace, [timestamp_label, parameter_of_interest])

    # Set a custom figure size
    fig = make_subplots(rows=1,
                        cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    # Style for the line plot
    sns.set_theme(style="darkgrid")
    sns.set(font_scale=1.90)

    # Plot line plot using dataframe columns
    # ------------ Physical Twin trajectory
    if parameter_of_interest == 'temperature(degrees)':
    # Difference of -3 to provide better visualization
        selected_pt[parameter_of_interest] = selected_pt[parameter_of_interest].apply(lambda x: x - 3)
    fig.add_trace(go.Scatter(x=selected_pt.loc[1:][timestamp_label], y=selected_pt.loc[1:][parameter_of_interest],
                             mode='lines+markers',
                             name='PT',
                             marker=dict(
                                 size=3,
                                 line_width=1,
                                 color = '#636EFA'
                             ),
                             line=dict(
                                 width=1,
                                 color='#636EFA'
                             )),
                  row=1, col=1)
    fig['layout']['yaxis']['title'] = parameter_of_interest

    # ------------- Digital Twin trajectory
    fig.add_trace(go.Scatter(x=selected_dt.loc[1:][timestamp_label], y=selected_dt.loc[1:][parameter_of_interest],
                             mode='lines+markers',
                             name='DT',
                             marker=dict(
                                 size=3,
                                 line_width=1,
                                 color='#FF7F0E'
                             ),
                             line=dict(
                                 width=1,
                                 color = '#FF7F0E'
                             )),
                  row=1, col=1)
    #fig['layout']['yaxis2']['title'] = parameter_of_interest
    fig['layout']['xaxis']['title'] = timestamp_label

    # Plot alignment with matching points
    for i in range(len(alignment["operation"])):
        if alignment["operation"][i] == "Match":
            if parameter_of_interest == "temperature(degrees)":
                fig.add_scatter(x=[float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                                y=[float(alignment[pt_param_interest][i])-3, float(alignment[dt_param_interest][i])],
                                mode='lines',
                                line=dict(color='#404040',
                                          dash='dash',
                                          width=0.5),
                                showlegend=False)
            else:
                fig.add_scatter(x=[float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                                y=[float(alignment[pt_param_interest][i]), float(alignment[dt_param_interest][i])],
                                mode='lines',
                                line=dict(color='#404040',
                                          dash='dash',
                                          width=0.5),
                                showlegend=False )

    # Distance between titles and axes to 0
    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)

    fig.update_layout(
        #xaxis_range=[0, 64],  # x axis range
        font=dict(
            size=12),  # Figure font
        legend=dict(  # Legend position
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

    annotation_text = f"<b>MAD:</b> {tolerance:.2f}<br><b>Gap:</b> ({open_gap:.1f}, {continue_gap:.1f})"
    fig.add_annotation(text=annotation_text,
                       align='left',
                       xref="paper", yref="paper",
                       bgcolor="white",
                       x=0.01, y=0.87,
                       showarrow=False,
                       borderpad=3,
                       font=dict(size=10))

    fig.show()
    fig.write_html(output_path.replace(".csv", "") + ".html")

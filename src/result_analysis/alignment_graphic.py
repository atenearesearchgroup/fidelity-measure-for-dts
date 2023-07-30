import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots

from util.dataframe_util import clean_df

FONT_SIZE = 28


def generate_alignment_graphic(alignment: pd.DataFrame,
                               dt_trace: pd.DataFrame,
                               pt_trace: pd.DataFrame,
                               params_of_interest: list,
                               timestamp_label: str,
                               mad: float,
                               open_gap: float,
                               continue_gap: float,
                               output_path: str = None,
                               engine: str = 'orca'):
    pt_timestamp = "pt-" + timestamp_label
    dt_timestamp = "dt-" + timestamp_label

    # Set a custom figure size
    fig = make_subplots(rows=len(params_of_interest),
                        cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    for index, param_of_interest in enumerate(params_of_interest, start=1):
        pt_param_interest = "pt-" + param_of_interest
        dt_param_interest = "dt-" + param_of_interest

        # Separate and clean the dataframe for plotting
        selected_pt = clean_df(pt_trace, [timestamp_label, param_of_interest])
        selected_dt = clean_df(dt_trace, [timestamp_label, param_of_interest])

        # Style for the line plot
        sns.set_theme(style="darkgrid")
        sns.set(font_scale=3)

        # Plot line plot using dataframe columns
        # ------------ Physical Twin trajectory
        if param_of_interest == 'temperature(degrees)':
            # Difference of -3 to provide better visualization
            selected_pt[param_of_interest] = selected_pt[param_of_interest].apply(lambda x: x - 3)

        if index == 1:
            show_legend = True
        else:
            show_legend = False

        fig.add_trace(go.Scatter(x=selected_pt.loc[1:][timestamp_label], y=selected_pt.loc[1:][param_of_interest],
                                 mode='lines+markers',
                                 name='Physical Twin',
                                 marker=dict(
                                     size=3,
                                     line_width=1,
                                     color='#636EFA'
                                 ),
                                 line=dict(
                                     width=1,
                                     color='#636EFA'
                                 ),
                                 showlegend=show_legend),
                      row=index, col=1)
        fig['layout'][f'yaxis{index}']['title'] = param_of_interest

        # ------------- Digital Twin trajectory
        fig.add_trace(go.Scatter(x=selected_dt.loc[1:][timestamp_label], y=selected_dt.loc[1:][param_of_interest],
                                 mode='lines+markers',
                                 name='Digital Twin',
                                 marker=dict(
                                     size=3,
                                     line_width=1,
                                     color='#FF7F0E'
                                 ),
                                 line=dict(
                                     width=1,
                                     color='#FF7F0E'
                                 ),
                                 showlegend=show_legend),
                      row=index, col=1)
        # fig['layout']['yaxis2']['title'] = parameter_of_interest

        # Plot alignment with matching points
        for i in range(len(alignment["operation"])):
            if alignment["operation"][i] == "Match":
                if param_of_interest == "temperature(degrees)":
                    fig.add_scatter(x=[float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                                    y=[float(alignment[pt_param_interest][i]) - 3,
                                       float(alignment[dt_param_interest][i])],
                                    mode='lines',
                                    line=dict(color='#404040',
                                              dash='dash',
                                              width=0.5),
                                    showlegend=False,
                                    row=index, col=1)
                else:
                    fig.add_scatter(x=[float(alignment[pt_timestamp][i]), float(alignment[dt_timestamp][i])],
                                    y=[float(alignment[pt_param_interest][i]), float(alignment[dt_param_interest][i])],
                                    mode='lines',
                                    line=dict(color='#404040',
                                              dash='dash',
                                              width=0.5),
                                    showlegend=False,
                                    row=index, col=1)

    fig['layout'][f'xaxis{len(params_of_interest)}']['title'] = timestamp_label
    # Distance between titles and axes to 0
    fig.update_yaxes(ticksuffix=" ", title_standoff=0)
    fig.update_xaxes(ticksuffix=" ", title_standoff=0)

    fig.update_layout(
        # xaxis_range=[0, 64],  # x axis range
        font=dict(
            size=FONT_SIZE),  # Figure font
        legend=dict(  # Legend position
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bordercolor='white',  # Set the border color
            borderwidth=3,  # Set the border width
        ),
        margin=dict(t=7, l=7, r=7, b=7))

    # annotation_text = f"<b>MAD:</b> {mad:.2f}" \
    #      #f"<br><b>Gap:</b> ({open_gap:.1f}, {continue_gap:.1f})"
    # fig.add_annotation(text=annotation_text,
    #                    align='left',
    #                    xref="paper", yref="paper",
    #                    bgcolor="white",
    #                    x=0.01, y=0.87,
    #                    showarrow=False,
    #                    borderpad=5,
    #                    font=dict(size=FONT_SIZE)
    #                    )

    # fig.show()
    # fig.write_html(output_path.replace(".csv", ".html"))
    if len(params_of_interest) > 1:
        fig.write_image(output_path.replace(".csv", ".pdf"), format="pdf", width=1750, height=3000, engine=engine)
    else:
        fig.write_image(output_path.replace(".csv", ".pdf"), format="pdf", width=1750, height=800, engine=engine)

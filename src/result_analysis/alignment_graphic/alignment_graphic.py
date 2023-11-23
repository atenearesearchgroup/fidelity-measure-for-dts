import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from util import clean_df


class AlignmentGraphics:
    PT_PREFIX = 'pt-'
    DT_PREFIX = 'dt-'
    FONT_SIZE = 28

    def __init__(self, alignment: pd.DataFrame,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 params_of_interest: list,
                 timestamp_label: str):
        self._alignment = alignment
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace
        self._params_of_interest = params_of_interest
        self._timestamp_label = timestamp_label

        self._visualization_indent = 1
        # 3 if self._params_of_interest[0] == 'temperature(degrees)' else 0

    def generate_alignment_graphic(self):

        # Set a custom figure size
        fig = make_subplots(rows=len(self._params_of_interest),
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.02)

        for index, param_interest in enumerate(self._params_of_interest, start=1):
            # Style for the line plot
            sns.set_theme(style="darkgrid")
            sns.set(font_scale=3)

            # Plot line plot using dataframe columns
            # ------------ Physical Twin trajectory
            self.insert_trace(self._pt_trace, index, param_interest,
                              fig, 'Physical Twin', '#3498DB', index == 1,
                              self._visualization_indent)

            # ------------- Digital Twin trajectory
            self.insert_trace(self._dt_trace, index, param_interest,
                              fig, 'Digital Twin', '#E74C3C', index == 1)

            fig['layout'][f'yaxis{index}']['title'] = param_interest

            self.insert_alignment_links(fig, index, param_interest,
                                        plot_color='rgba(126, 255, 84, 0.7)',
                                        visualization_indent=self._visualization_indent)

        fig['layout'][f'xaxis{len(self._params_of_interest)}']['title'] = self._timestamp_label

        # Distance between titles and axes to 0
        fig.update_yaxes(ticksuffix=" ", title_standoff=0)
        fig.update_xaxes(ticksuffix=" ", title_standoff=0)

        fig.update_layout(
            # xaxis_range=[0, 64],  # x axis range
            font=dict(
                size=self.FONT_SIZE),  # Figure font
            legend=dict(  # Legend position
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bordercolor='white',  # Set the border color
                borderwidth=3,  # Set the border width
            ),
            margin=dict(t=7, l=7, r=7, b=7))

        return fig

    def insert_trace(self, trace: pd.DataFrame,
                     row_index: int,
                     param_interest: str,
                     fig: Figure,
                     plot_label: str = '',
                     plot_color: str = '#000000',  # Black
                     show_legend: bool = False,
                     visualization_indent: int = 0):

        selected_pt = clean_df(trace, [self._timestamp_label, param_interest])

        if visualization_indent > 0:
            selected_pt[param_interest] = selected_pt[param_interest].apply(
                lambda x: x - visualization_indent)

        fig.add_trace(go.Scatter(x=selected_pt[self._timestamp_label],
                                 y=selected_pt[param_interest],
                                 mode='lines+markers',
                                 name=plot_label,
                                 marker={
                                     "size": 5,
                                     "line_width": 1,
                                     "color": plot_color
                                 },
                                 line={
                                     "width": 3,
                                     "color": plot_color
                                 },
                                 showlegend=show_legend),
                      row=row_index, col=1)

    def insert_alignment_links(self, fig: Figure,
                               row_index: int,
                               param_interest: int,
                               plot_color: str = '#000000',  # Black
                               visualization_indent: int = 0):
        """
        Fill this function in any subclass if you wish to add the alignment links between the
        traces.

        :param fig:
        :param row_index:
        :param param_interest:
        :param plot_color:
        :param visualization_indent:
        :return:
        """
        pass

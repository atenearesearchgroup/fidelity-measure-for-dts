import pandas as pd
import plotly.graph_objects as go
from _plotly_utils.colors import sample_colorscale
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
        self._params_of_interest = params_of_interest
        self._timestamp_label = timestamp_label

        self._alignment = clean_df(alignment)
        self._dt_trace = clean_df(dt_trace)
        self._pt_trace = clean_df(pt_trace)

        self._visualization_indent = 30

    def generate_alignment_graphic(self):
        colors = sample_colorscale('Sunset', [0.20, 0.70])

        # Set a custom figure size
        fig = make_subplots(rows=len(self._params_of_interest),
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.02)

        for index, param_interest in enumerate(self._params_of_interest, start=1):
            # Style for the line plot

            self.insert_alignment_links(fig, index, param_interest,
                                        plot_color='rgba(80, 80, 124, 0.3)',
                                        visualization_indent=self._visualization_indent)

            # Plot line plot using dataframe columns
            # ------------ Physical Twin trajectory
            self.insert_trace(self._pt_trace, index, param_interest,
                              fig, 'Physical Twin', colors[0], index == 1,
                              self._visualization_indent,
                              marker_symbol='circle')

            # ------------- Digital Twin trajectory
            self.insert_trace(self._dt_trace, index, param_interest,
                              fig, 'Digital Twin', colors[1], index == 1,
                              marker_symbol='star-square')

            fig['layout'][f'yaxis{index}']['title'] = f'{param_interest} (mm)'

        fig['layout'][f'xaxis{len(self._params_of_interest)}']['title'] = self._timestamp_label

        # Distance between titles and axes to 0
        fig.update_yaxes(showline=True, linewidth=1, linecolor='gray', ticksuffix=" ",
                         title_standoff=2)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', ticksuffix=" ",
                         title_standoff=2)

        fig.update_layout(
            # xaxis_range=[0, 64],  # x axis range
            template='plotly_white',
            font=dict(
                size=self.FONT_SIZE),  # Figure font
            legend=dict(  # Legend position
                yanchor="top",
                y=1.00,
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
                     visualization_indent: float = 0,
                     marker_symbol: str = 'circle'):

        # selected_pt = clean_df(trace, [self._timestamp_label, param_interest])
        selected_pt = trace.loc[:, [self._timestamp_label, param_interest]]

        if visualization_indent > 0 and selected_pt[param_interest].dtype in ['float64', 'int64']:
            selected_pt[param_interest] = selected_pt[param_interest].apply(
                lambda x: x - visualization_indent)

        fig.add_trace(go.Scatter(x=selected_pt[self._timestamp_label],
                                 y=selected_pt[param_interest],
                                 mode='lines+markers',
                                 name=plot_label,
                                 marker={
                                     # "size": 10,
                                     "line_width": 0.5,
                                     "color": plot_color,
                                     "symbol": marker_symbol
                                 },
                                 line={
                                     "width": 5,
                                     "color": plot_color
                                 },
                                 showlegend=show_legend),
                      row=row_index, col=1)

    def insert_alignment_links(self, fig: Figure,
                               row_index: int,
                               param_interest: int,
                               plot_color: str = '#000000',  # Black
                               visualization_indent: float = 0):
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

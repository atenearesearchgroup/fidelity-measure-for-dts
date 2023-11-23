from plotly.graph_objs import Figure

from result_analysis.alignment_graphic.alignment_graphic import AlignmentGraphics

FONT_SIZE = 28


class DynamicTimeWarpingAlignmentGraphics(AlignmentGraphics):
    def insert_alignment_links(self, fig: Figure,
                               row_index: int,
                               param_interest: str,
                               plot_color: str = '#000000',
                               visualization_indent: int = 0):
        pt_timestamp = self.PT_PREFIX + self._timestamp_label
        dt_timestamp = self.DT_PREFIX + self._timestamp_label

        pt_param_interest = self.PT_PREFIX + param_interest
        dt_param_interest = self.DT_PREFIX + param_interest

        # Plot alignment with matching points
        for i in range(len(self._alignment[pt_param_interest])):
            y_var = [float(self._alignment[pt_param_interest][i]),
                     float(self._alignment[dt_param_interest][i])]
            if visualization_indent > 0:
                y_var[0] -= visualization_indent

            fig.add_scatter(
                x=[float(self._alignment[pt_timestamp][i]),
                   float(self._alignment[dt_timestamp][i])],
                y=y_var,
                mode='lines',
                line=dict(color=plot_color,
                          # dash='longdash',
                          width=0.0001),
                showlegend=False,
                row=row_index, col=1)

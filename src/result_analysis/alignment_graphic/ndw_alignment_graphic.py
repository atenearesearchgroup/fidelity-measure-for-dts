from plotly.graph_objs import Figure

from result_analysis.alignment_graphic.alignment_graphic import AlignmentGraphics


class NeedlemanWunschAlignmentGraphics(AlignmentGraphics):

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
        for i in range(len(self._alignment["operation"])):
            if self._alignment["operation"][i] == "Match":
                y_var = [self._alignment[pt_param_interest][i],
                         self._alignment[dt_param_interest][i]]

                if visualization_indent > 0 and not isinstance(y_var[0], str) and \
                        (isinstance(y_var[0], (float, int)) or y_var[0].dtype in ['int32', 'int64',
                                                                                  'float64']):
                    y_var[0] -= visualization_indent

                fig.add_scatter(
                    x=[float(self._alignment[pt_timestamp][i]),
                       float(self._alignment[dt_timestamp][i])],
                    y=y_var,
                    mode='lines',
                    line=dict(color=plot_color,
                              dash='solid',
                              width=0.1),
                    showlegend=False,
                    row=row_index, col=1)

import multiprocessing

import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

from batch_processing.alg_config.alignment_config import AlignmentConfiguration
from metrics import NeedlemanWunschAlignmentMetricsLCA, NeedlemanWunschAlignmentMetrics
from systems import Lift


class AlignmentDashboard:
    def __init__(self, window_size: int,
                 conf: AlignmentConfiguration,
                 manager: multiprocessing.Manager):
        super().__init__(window_size, conf, manager)
        alignments = 3

        manager = multiprocessing.Manager()
        self._fig_queue = manager.list()
        self._statistical_results = manager.list()
        self._max_stat_counter = 100

        dash_thread = multiprocessing.Process(target=self.run_app, args=(self._fig_queue,
                                                                         self._statistical_results,))

        # Start the Dash app thread
        dash_thread.start()

    @staticmethod
    def run_app(fig_queue, statistical_results):
        STATISTICAL_PLOTS = ['PERCENTAGE_MATCHED', 'FRECHET', 'EUCLIDEAN']

        app = dash.Dash(__name__)

        alignments = 3

        app.layout = html.Div([
            # First row with alignments
            html.Div([
                dcc.Graph(id='align' + str(i), config={'displayModeBar': False})
                for i in range(alignments)
            ], className='row'),

            html.Div([
                dcc.Graph(id=plot_name, config={'displayModeBar': False})
                for plot_name in STATISTICAL_PLOTS
            ], className='row'),

            # Interval update
            dcc.Interval(
                id='interval-component',
                interval=1000,  # Update every 1 second
                n_intervals=0
            )
        ])
        outputs = [Output('align' + str(i), 'figure') for i in range(alignments)] + \
                  [Output(stat_plot, 'figure') for stat_plot in STATISTICAL_PLOTS]
        app.callback(outputs,
                     [Input('interval-component', 'n_intervals')]) \
            (AlignmentDashboard.update_plot(fig_queue, statistical_results))

        host = 'localhost'  # Change this to your server's host
        port = 8052  # Change this to your desired port
        app.run(debug=True, host=host, port=port)

    @staticmethod
    def update_plot(fig_queue, statistical_results):
        # STATISTICAL_PLOTS = ['PERCENTAGE_MATCHED', 'FRECHET', 'EUCLIDEAN']
        #
        # df = pd.DataFrame(list(statistical_results))
        # if len(df) > 100:
        #     df = df[len(df) - 100:]
        #
        # if len(fig_queue) > 3:
        #     fig_queue = fig_queue[-3:]
        #
        # # Create a Plotly figure with the updated data
        # statistical_figs = []
        # if not df.empty:
        #     for stats in STATISTICAL_PLOTS:
        #         fig = go.Figure(data=[go.Scatter(x=df[stats],
        #                                          y=df[stats],
        #                                          mode='lines+markers')])
        #         fig.update_layout(title='Real-Time Data Plot', xaxis_title='Time',
        #                           yaxis_title='Value')
        #         statistical_figs.append(go.Figure(fig))

        # if fig_queue and statistical_figs:
        #     final_list = fig_queue.extend(statistical_figs)
        #     if final_list and len(final_list) < 6:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()
        # else:
        #     return *final_list,

    def align(self):
        super().align()
        STATISTICAL_PLOTS = ['PERCENTAGE_MATCHED', 'FRECHET', 'EUCLIDEAN']

        self._fig_queue.append(go.Figure(self._alignment_fig))
        if isinstance(self._conf.system, Lift):
            alignment_results = NeedlemanWunschAlignmentMetricsLCA(self._alignment_df,
                                                                   pd.DataFrame(self._dt_trace),
                                                                   pd.DataFrame(self._pt_trace),
                                                                   self._conf.system,
                                                                   self._conf.params)
            if len(self._statistical_results) <= 0:
                self._statistical_results = [
                    {STATISTICAL_PLOTS[0]: alignment_results.percentage_matched_snapshots_lca,
                     STATISTICAL_PLOTS[1]: alignment_results.frechet_lca,
                     STATISTICAL_PLOTS[2]: alignment_results.p2p_mean_lca}]
            else:
                self._statistical_results.append(
                    {STATISTICAL_PLOTS[0]: alignment_results.percentage_matched_snapshots_lca,
                     STATISTICAL_PLOTS[1]: alignment_results.frechet_lca,
                     STATISTICAL_PLOTS[2]: alignment_results.p2p_mean_lca})
            # self._statistical_results.append(
            #     [{STATISTICAL_PLOTS[0]: alignment_results.percentage_matched_snapshots_lca,
            #       STATISTICAL_PLOTS[1]: alignment_results.frechet_lca,
            #       STATISTICAL_PLOTS[2]: alignment_results.p2p_mean_lca}], ignore_index=True)
        else:
            alignment_results = NeedlemanWunschAlignmentMetrics(self._alignment_df, self._dt_trace,
                                                                self._pt_trace,
                                                                self._conf.system,
                                                                self._conf.params)
            self._statistical_results.append(
                [{STATISTICAL_PLOTS[0]: alignment_results.percentage_matched_snapshots,
                  STATISTICAL_PLOTS[1]: alignment_results.frechet,
                  STATISTICAL_PLOTS[2]: alignment_results.p2p_mean}], ignore_index=True)

from algorithm.config.factory import ConfigFactory
from batch.mode.imode import AlignmentMode
from batch.mode.trace import TraceAlignmentMode
from batch.mode.window import WindowAlignmentMode
from batch.modifiers.anomaly import AnomalyWrapper
from batch.modifiers.delay import DelayWrapper


class BatchFactory:
    @staticmethod
    def get_batch_configuration(args) -> AlignmentMode:
        alignment_config = ConfigFactory.get_algorithm_configuration(args)
        labels = alignment_config.get_hyperparameters_labels()
        if WindowAlignmentMode.INTERVAL_PERIOD in labels:
            batch_alignment = WindowAlignmentMode(alignment_config)
        else:
            batch_alignment = TraceAlignmentMode(alignment_config)
        if AnomalyWrapper.LEN_ANOMALY in labels:
            batch_alignment.add_trace_modifier(AnomalyWrapper())
        if DelayWrapper.LEN_DELAY in labels:
            batch_alignment.add_trace_modifier(DelayWrapper())

        return batch_alignment

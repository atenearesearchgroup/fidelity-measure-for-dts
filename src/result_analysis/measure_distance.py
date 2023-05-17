import numpy as np
import pandas as pd
import similaritymeasures
from scipy.spatial import distance

from systems_config.system import SystemBase


def measure_distance(alignment: pd.DataFrame,
                     dt_trace: pd.DataFrame,
                     pt_trace: pd.DataFrame,
                     parameters: list,
                     cps: SystemBase):
    pt_params = ["pt-" + p for p in parameters]
    dt_params = ["dt-" + p for p in parameters]

    # Initialize resulting variables
    frechet_euclidean = 0
    euclidean_mean = 0
    euclidean_std = 0
    mismatch_counter = 0

    frechet_euclidean_out_lca = 0
    euclidean_mean_lca = 0
    euclidean_std_lca = 0
    percentage_matched_out_lca = 100

    # Initialize auxiliary variables for gaps
    gap_cont = 0
    gap_length = []

    # Process alignment statistics: mismatch and gaps
    for i in range(len(alignment["operation"])):
        if alignment["operation"][i] == "Insertion" or alignment["operation"][i] == "Deletion":
            gap_cont += 1  # Increase gap counter
        else:
            if gap_cont > 0:  # Gap ended
                gap_length.append(gap_cont)  # Add gap length
                gap_cont = 0  # Reset counter
            if alignment["operation"][i] == "Mismatch":
                mismatch_counter += 1

    # Get aligned snapshots (matches)
    match_condition = alignment["operation"] == "Match"

    snapshots_dt = alignment.loc[match_condition, dt_params].astype(float)
    snapshots_dt.columns = snapshots_dt.columns.str.replace('dt-', '')

    snapshots_pt = alignment.loc[match_condition, pt_params].astype(float)
    snapshots_pt.columns = snapshots_pt.columns.str.replace('pt-', '')

    # ALIGNMENT MATCHES
    percentage_matched = snapshots_pt.shape[0] / max(pt_trace[pt_trace != ' '].shape[0],
                                                     dt_trace[dt_trace != ' '].shape[0]) * 100
    print(f"Number of matched ({snapshots_dt.shape[0]},{snapshots_pt.shape[0]}) "
          f"- Total ({dt_trace[dt_trace != ' '].shape[0]},{pt_trace[pt_trace != ' '].shape[0]})"
          f"- {percentage_matched:.2f} % of matched")

    # ALIGNMENT MATCHES OUTSIDE LOW-COMPLEXITY AREAS (lca)
    if cps.is_low_complexity():
        pt_matched_out_lca = snapshots_pt.loc[~cps.is_low_complexity(snapshots_pt[parameters]), parameters]
        total_out_lca = pt_trace.loc[~cps.is_low_complexity(pt_trace[parameters]), parameters]
        percentage_matched_out_lca = pt_matched_out_lca.shape[0] / total_out_lca.shape[0] * 100

        print(f"Number of matched in relevant areas - Total ({pt_matched_out_lca.shape[0]},{total_out_lca.shape[0]})"
              f"- {percentage_matched_out_lca:.2f} % of matched")

    if snapshots_dt.shape[0] > 0 and snapshots_pt.shape[0] > 0:
        snapshots_dt_output = snapshots_dt.to_numpy()
        snapshots_pt_output = snapshots_pt.to_numpy()
        frechet_euclidean = similaritymeasures.frechet_dist(snapshots_dt_output, snapshots_pt_output, 2)
        print(f"Frechet distance using Euclidean distance: {frechet_euclidean:.4f}")

        euclidean = [distance.cdist([snapshots_dt_output[i]], [snapshots_pt_output[i]], 'cityblock')[0]
                     for i in range(len(snapshots_dt_output))]
        euclidean_mean = np.mean(euclidean)
        euclidean_std = np.std(euclidean)
        print(f"Euclidean distance: {euclidean_mean:.4f} StDev: {euclidean_std:.4f}")

        # Measure Frèchet distance outside Low-Complexity Areas
        if cps.is_low_complexity():
            merge_lca_condition = ~cps.is_low_complexity(snapshots_pt[parameters])
            dt_matched_out_lca_output = snapshots_dt.loc[merge_lca_condition, parameters].to_numpy()
            pt_matched_out_lca_output = snapshots_pt.loc[merge_lca_condition, parameters].to_numpy()

            euclidean_lca = [
                distance.cdist([dt_matched_out_lca_output[i]], [pt_matched_out_lca_output[i]], 'cityblock')[0]
                for i in range(len(dt_matched_out_lca_output))]
            if euclidean_lca:
                frechet_euclidean_out_lca = similaritymeasures.frechet_dist(dt_matched_out_lca_output,
                                                                            pt_matched_out_lca_output, 2)
                euclidean_mean_lca = np.mean(euclidean_lca)
                euclidean_std_lca = np.std(euclidean_lca)

            print(f"Frechet distance in relevant areas using Euclidean distance: {frechet_euclidean_out_lca:.4f}")
            print(f"Euclidean distance: {euclidean_mean_lca:.4f} StDev: {euclidean_std_lca:.4f}")

    # ALIGNMENT MISMATCHES
    percentage_mismatched = mismatch_counter / min(len(pt_trace[pt_trace != ' ']),
                                                   len(dt_trace[dt_trace != ' '])) * 100
    print(f"Number of mismatches {mismatch_counter} "
          f"- {percentage_mismatched:.2f} % of mismatches")

    # ALIGNMENT GAPS
    if gap_length:
        gap_number = len(gap_length)
        gap_total_numer = np.sum(gap_length)
        gap_mean_length = np.mean(gap_length)
        gap_std_length = np.std(gap_length)
        percentage_gaps = 100 - percentage_matched - percentage_mismatched

        print(f"Number of gaps: groups {gap_number}, individual {gap_total_numer} "
              f"- Percentage: {percentage_gaps:.2f} %\n"
              f"- Mean length {gap_mean_length:.2f} - Std {gap_std_length:.2f} "
              f"- Max length {np.max(gap_length)} - Min length {np.min(gap_length)}")
    else:
        gap_number = 0
        gap_total_numer = 0
        gap_mean_length = 0
        gap_std_length = 0

    return [percentage_matched, frechet_euclidean, euclidean_mean, euclidean_std, percentage_mismatched, gap_number,
            gap_total_numer, gap_mean_length, gap_std_length, percentage_matched_out_lca, frechet_euclidean_out_lca,
            euclidean_mean_lca, euclidean_std_lca]

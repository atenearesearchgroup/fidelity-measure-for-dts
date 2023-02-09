import numpy as np
import pandas as pd
import similaritymeasures
from scipy.spatial import distance


def measure_distance(alignment: pd.DataFrame,
                     dt_trace: pd.DataFrame,
                     pt_trace: pd.DataFrame,
                     parameters: list):
    pt_param = "pt-"
    dt_param = "dt-"

    # Initialize resulting variables
    frechet_euclidean = -1
    euclidean_mean = 0
    euclidean_std = 0
    mismatch_counter = 0

    # Initialize auxiliary variables for gaps
    gap_cont = 0
    gap_length = []
    # Initialize auxiliary arrays for matched points
    snapshots_dt = []
    snapshots_pt = []
    for _ in range(len(parameters)):
        snapshots_dt.append([])
        snapshots_pt.append([])

    # Process alignment statistics: match, mismatch and gaps
    for i in range(len(alignment["operation"])):
        if alignment["operation"][i] == "Insertion" or alignment["operation"][i] == "Deletion":
            gap_cont += 1  # Increase gap counter
        else:
            if gap_cont > 0:  # Gap ended
                gap_length.append(gap_cont)  # Add gap length
                gap_cont = 0  # Reset counter
            if alignment["operation"][i] == "Match":
                for j in range(len(parameters)):  # Add matched points to lists
                    snapshots_dt[j].append(alignment[dt_param + parameters[j]][i])
                    snapshots_pt[j].append(alignment[pt_param + parameters[j]][i])
            elif alignment["operation"][i] == "Mismatch":
                mismatch_counter += 1  # Increase mismatch counter

    # ALIGNMENT MATCHES
    percentage_matched = len(snapshots_pt[0]) / max(len(pt_trace[pt_trace != ' ']),
                                                    len(dt_trace[dt_trace != ' '])) * 100
    print(f"Number of matched ({len(snapshots_dt[0])},{len(snapshots_pt[0])}) "
          f"- Total ({len(dt_trace[dt_trace != ' '])},{len(pt_trace[pt_trace != ' '])})"
          f"- {percentage_matched:.2f} % of matched")

    if snapshots_dt:
        snapshots_dt_output = np.zeros((len(snapshots_dt[0]), len(parameters)))
        snapshots_pt_output = np.zeros((len(snapshots_pt[0]), len(parameters)))
        for i in range(len(parameters)):
            snapshots_dt_output[:, i] = snapshots_dt[i]
            snapshots_pt_output[:, i] = snapshots_pt[i]

        frechet_euclidean = similaritymeasures.frechet_dist(snapshots_dt_output, snapshots_pt_output, 2)
        print(f"Frechet distance using Euclidean distance: {frechet_euclidean:.4f}")
        # frechet_manhattan = similaritymeasures.frechet_dist(snapshots_dt_output, snapshots_pt_output, 1)
        # print(f"Frechet distance using Manhattan distance: {frechet_manhattan:2f}")

        manhattan = []
        euclidean = []
        for i in range(len(snapshots_dt_output)):
            manhattan.append(distance.cdist([snapshots_dt_output[i]], [snapshots_pt_output[i]], 'cityblock')[0])
            euclidean.append(distance.cdist([snapshots_dt_output[i]], [snapshots_pt_output[i]], 'euclidean')[0])

        euclidean_mean = np.mean(euclidean)
        euclidean_std = np.std(euclidean)
        print(f"Euclidean distance: {euclidean_mean:.4f} StDev: {euclidean_std:.4f}")
        # print(f"Manhattan distance: {np.mean(manhattan)} StDev: {np.std(manhattan)}")

    # ALIGNMENT MISMATCHES
    percentage_mismatched = mismatch_counter / max(len(pt_trace[pt_trace != ' ']),
                                                   len(dt_trace[dt_trace != ' '])) * 100
    print(f"Number of mismatches {mismatch_counter} "
          f"- {percentage_mismatched:.2f} % of mismatches")

    # ALIGNMENT GAPS
    gap_number = len(gap_length)
    gap_total_numer = np.sum(gap_length)
    gap_mean_length = np.mean(gap_length)
    gap_std_length = np.std(gap_length)
    percentage_gaps = 100 - percentage_matched - percentage_mismatched
    print(f"Number of gaps: groups {gap_number}, individual {gap_total_numer} "
          f"- Percentage: {percentage_gaps:.2f} %\n"
          f"- Mean length {gap_mean_length:.2f} - Std {gap_std_length:.2f} "
          f"- Max length {np.max(gap_length)} - Min length {np.min(gap_length)}")

    return [percentage_matched, frechet_euclidean, euclidean_mean, euclidean_std, percentage_mismatched, \
        gap_number, gap_total_numer, gap_mean_length, gap_std_length]

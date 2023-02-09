import os

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
    euclidean = 0

    # Initialize auxiliary arrays
    snapshots_dt = []
    snapshots_pt = []
    for _ in range(len(parameters)):
        snapshots_dt.append([])
        snapshots_pt.append([])

    # Gets a list of all the matched points which are in the operation column
    for i in range(len(alignment["operation"])):
        if alignment["operation"][i] == "Match":
            for j in range(len(parameters)):
                snapshots_dt[j].append(alignment[dt_param + parameters[j]][i])
                snapshots_pt[j].append(alignment[pt_param + parameters[j]][i])

    print(f"Number of matched ({len(snapshots_dt[0])},{len(snapshots_pt[0])}) "
          f"- Total ({len(dt_trace[dt_trace != ' '])},{len(pt_trace[pt_trace != ' '])})")

    percentage_matched = len(snapshots_pt[0]) / min(len(pt_trace[pt_trace != ' ']),
                                                    len(dt_trace[dt_trace != ' '])) * 100
    print(f"{percentage_matched:2f} % of matched")

    if snapshots_dt:
        snapshots_dt_output = np.zeros((len(snapshots_dt[0]), len(parameters)))
        snapshots_pt_output = np.zeros((len(snapshots_pt[0]), len(parameters)))
        for i in range(len(parameters)):
            snapshots_dt_output[:, i] = snapshots_dt[i]
            snapshots_pt_output[:, i] = snapshots_pt[i]

        frechet_euclidean = similaritymeasures.frechet_dist(snapshots_dt_output, snapshots_pt_output, 2)
        print(f"Frechet distance using Euclidean distance: {frechet_euclidean:2f}")
        # frechet_manhattan = similaritymeasures.frechet_dist(snapshots_dt_output, snapshots_pt_output, 1)
        # print(f"Frechet distance using Manhattan distance: {frechet_manhattan:2f}")

        manhattan = []
        euclidean = []
        for i in range(len(snapshots_dt_output)):
            manhattan.append(distance.cdist([snapshots_dt_output[i]], [snapshots_pt_output[i]], 'cityblock')[0])
            euclidean.append(distance.cdist([snapshots_dt_output[i]], [snapshots_pt_output[i]], 'euclidean')[0])

        print(f"Euclidean distance: {np.mean(euclidean):2f} StDev: {np.std(euclidean):2f}")
        # print(f"Manhattan distance: {np.mean(manhattan)} StDev: {np.std(manhattan)}")

    return percentage_matched, frechet_euclidean, np.mean(euclidean), np.std(euclidean)

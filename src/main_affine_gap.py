import argparse
import os
import time

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

import util.csv_util as cu
import util.file_util as fu
from algorithm.needleman_wunsch_affine_gap import NeedlemanWunschAffineGap
from result_analysis.alignment_graphic import generate_alignment_graphic
from result_analysis.measure_distance import measure_distance
from result_analysis.statistical_graphics import generate_statistical_info_stairs
from systems_config.lift import Lift
from util.float_util import get_input_values_list

# nohup python -u my_script.py > program.out 2>&1 &

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", help="It processes the alignment and generates figures as image files")
    args = parser.parse_args()

    # FILE PATHS
    current_directory = os.path.join(os.getcwd(), "")
    input_directory = current_directory + "resources/input/lift/"
    output_directory = current_directory + "resources/output/lift/"

    # DIGITAL TWIN
    dt_path = input_directory + "04.5-simulation/"
    dt_file = ["cutBajada_4_0_4.csv"]

    # PHYSICAL TWIN
    pt_path = input_directory + "03.55-derived_values/"
    pt_files = ["Bajada_4_0_4_01.csv"]

    # ANALYSIS PARAMETERS
    timestamp_label = "timestamp(s)"
    param_interest = "accel(m/s2)"

    # INPUT PARAMETERS

    # Maximum Acceptable Distance : MAD
    max_acceptable_dist = np.arange(0.15, 0.16, 0.02)
    # Weight for Low complexity areas
    low = np.arange(200, 205, 5)
    # Weights for Affine Gap
    init_gap = np.arange(0.0, 0.1, 0.1)
    continue_gap = init_gap / 11

    input_values = get_input_values_list(max_acceptable_dist, low, init_gap, continue_gap)

    # Headers for the analysis file
    headers = ["init_gap_cost", "gap_cost", "low", "tolerance", "%matched", "frechet", "match_mean", "match_std",
               "%mismatch", "gap_groups", "gap_individual", "gap_length_mean", "gap_length_std", "%matched_out_lca",
               "frechet_out_lca", "match_mean_out_lca", "match_std_out_lca"]

    # Iterate over Physical Twin Files against Digital Twins'
    for i in range(len(pt_files)):
        for pt_file in fu.list_directory_files(pt_path, ".csv", pt_files[i]):
            # Unique filename combining both in format : <fileAfileB>
            output_filename = dt_file[i][:dt_file[i].index(".csv")] + pt_file[
                                                                      :pt_file.index(".csv")]  # + param_interest
            # Output directory combined with filename and extension : path/to/output/fileAfileB.csv
            output_dir_filename = output_directory + output_filename + ".csv"

            # File with statistical outputs for each alignment
            file_writer, writer = cu.get_writer(output_dir_filename, ",", 'w')
            writer.writerow(headers)

            # DT and PT traces in dict
            dt_trace = pd.read_csv(dt_path + dt_file[i])
            pt_trace = pd.read_csv(pt_path + pt_file)

            for inputs in input_values:
                mad_curr = {param_interest: inputs[0],
                            timestamp_label: inputs[0]}
                low_curr = inputs[1]
                init_curr = inputs[2]
                cont_curr = inputs[3]

                output_dir_filename_gap = output_directory + output_filename + "-{:.2f}".format(
                    init_curr) + "-{:.2f}".format(cont_curr) + "-{:.2f}".format(low_curr) + "-{:.2f}".format(
                    mad_curr[param_interest]) + ".csv"

                # --- CALCULATE ALIGNMENT - MAIN ALGORITHM ---
                start_time = time.time()

                cps = Lift()

                ndw = NeedlemanWunschAffineGap(dt_trace.to_dict('records'),
                                               pt_trace.to_dict('records'),
                                               cps,
                                               initiate_gap=init_curr,
                                               continue_gap=cont_curr,
                                               low=low_curr,
                                               mad=mad_curr)

                alignment_df = ndw.calculate_alignment()

                print(f"--- SCENARIO: {output_filename} ---")
                print(
                    f"--- Init gap {init_curr}, Continue gap {cont_curr} : {(time.time() - start_time):.2f} seconds ---")

                alignment_df.to_csv(output_dir_filename_gap, index=False, encoding='utf-8', sep=',')

                if args.figures:
                    # --- GRAPHIC GENERATION ---
                    generate_alignment_graphic(alignment_df, dt_trace, pt_trace, param_interest, timestamp_label,
                                               output_path=output_dir_filename_gap,
                                               tolerance=mad_curr[param_interest],
                                               open_gap=init_curr, continue_gap=cont_curr)

                # --- DISTANCE ANALYSIS ---
                statistical_values = measure_distance(alignment_df, dt_trace, pt_trace,
                                                      [param_interest], cps)
                row = [init_curr, cont_curr, low_curr, mad_curr[param_interest]]
                row.extend(statistical_values)
                writer.writerow(row)

            # --- GAP AND PERCENTAGE MATCHED COMPARISON ---
            file_writer.close()
            if args.figures:
                generate_statistical_info_stairs('tolerance', pd.read_csv(output_dir_filename, index_col=False),
                                                 make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.0))

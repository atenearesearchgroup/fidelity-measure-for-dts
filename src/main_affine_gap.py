import os
import time

import numpy as np
import pandas as pd

import util.file_util as fu
import util.csv_util as cu
from algorithm.lift_case_study import LiftCaseStudy
from algorithm.needleman_wunsch_affine_gap import NeedlemanWunschAffineGap
from process_results.alignment_graphic import generate_graphic
from process_results.distance_measure import measure_distance
from process_results.process_results import generate_statistical_info_graphic

# nohup python -u my_script.py > program.out 2>&1 &

if __name__ == "__main__":

    # FILE PATHS
    current_directory = os.path.join(os.getcwd(), "")
    input_directory = current_directory + "resources/input/lift/"
    output_directory = current_directory + "resources/output/lift/"

    # DIGITAL TWIN
    dt_path = input_directory + "04.5-simulation/"
    dt_file = ["Bajada_4_0_4.csv"]
        #, "Bajada_4_2_0_2_4.csv", "Bajada_4_3_2_1_0_1_2_3_4.csv"]

    # PHYSICAL TWIN
    pt_path = input_directory + "03-derived_values/"
    pt_files = ["Bajada_4_0_4_09"]
        #, "Bajada_4_2_0_2_4", "Bajada_4_3_2_1_0_1_2_3_4"]

    # ANALYSIS PARAMETERS
    timestamp_label = "timestamp(s)"
    param_interest = "accel(m/s2)"

    # Headers for the analysis file
    headers = ["init_gap_cost", "gap_cost", "low", "%matched", "frechet", "match_mean", "match_std", "%mismatch", "gap_groups",
               "gap_individual", "gap_length_mean", "gap_length_std" ]

    for i in range(len(pt_files)):
        for pt_file in fu.list_directory_files(pt_path, ".csv", pt_files[i]):
            # Combining the two filenames for the aligned output
            output_filename = dt_file[i][:dt_file[i].index(".csv")] + pt_file[:pt_file.index(".csv")]
            output_dir_filename = output_directory + output_filename  + ".csv"

            # Analysis file for different gap values initialization
            file_writer, writer = cu.get_writer(output_dir_filename, ",", 'w')
            writer.writerow(headers)

            # DT and PT traces in dict
            dt_trace = pd.read_csv(dt_path + dt_file[i])
            pt_trace = pd.read_csv(pt_path + pt_file)

            # You could try with different values of gap
            for init_gap in np.arange(0, 0.05, 0.05):
                for continue_gap in np.arange(-0.1, -0.05, 0.05):
                    for low in np.arange(10, 15, 5):
                        output_dir_filename_gap = output_directory + output_filename + "-{:.2f}".format(init_gap) + "-{:.2f}".format(continue_gap) + "-{:.2f}".format(low)  +".csv"

                        # --- CALCULATE ALIGNMENT - MAIN ALGORITHM ---
                        start_time = time.time()

                        ndw = NeedlemanWunschAffineGap(dt_trace.to_dict('records'),
                                                       pt_trace.to_dict('records'),
                                                       LiftCaseStudy(),
                                                       initiate_gap=init_gap,
                                                       continue_gap=continue_gap,
                                                       low=low)
                        alignment_df = ndw.calculate_alignment()

                        print(f"--- Init gap {init_gap}, Continue gap {continue_gap} : {(time.time() - start_time):2f} seconds ---")

                        alignment_df.to_csv(output_dir_filename_gap, index=False, encoding='utf-8', sep=',')

                        # --- GRAPHIC GENERATION ---
                        generate_graphic(alignment_df, dt_trace, pt_trace, param_interest, timestamp_label,
                                         output_path=output_dir_filename_gap)

                        # --- DISTANCE ANALYSIS ---
                        statistical_values = measure_distance(alignment_df, dt_trace, pt_trace,
                                                                                       [param_interest])
                        row = [init_gap, continue_gap, low]
                        row.extend(statistical_values)
                        writer.writerow(row)

            # --- GAP AND PERCENTAGE MATCHED COMPARISON ---
            file_writer.close()
            generate_statistical_info_graphic('gap_cost', output_dir_filename)




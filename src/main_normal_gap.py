import os
import time

import numpy as np
import pandas as pd
from cps_configuration.lift import Lift

import util.csv_util as cu
import util.file_util as fu
from algorithm.needleman_wunsch_tolerance import NeedlemanWunschTolerance
from result_analysis.alignment_graphic import generate_alignment_graphic
from result_analysis.measure_distance import measure_distance
from result_analysis.statistical_graphics import generate_statistical_info_graphic

if __name__ == "__main__":

    # FILE PATHS
    current_directory = os.path.join(os.getcwd(), "")
    input_directory = current_directory + "resources\\input\\lift\\"
    output_directory = current_directory + "resources\\output\\lift\\"

    # DIGITAL TWIN
    dt_path = input_directory + "04.5-simulation\\"
    dt_file = ["Bajada_4_0_4.csv", "Bajada_4_2_0_2_4.csv", "Bajada_4_3_2_1_0_1_2_3_4.csv"]

    # PHYSICAL TWIN
    pt_path = input_directory + "03-derived_values\\"
    pt_files = ["Bajada_4_0_4", "Bajada_4_2_0_2_4", "Bajada_4_3_2_1_0_1_2_3_4"]

    # ANALYSIS PARAMETERS
    timestamp_label = "timestamp(s)"
    param_interest = "accel(m/s2)"

    # Headers for the analysis file
    headers = ["gap", "%matched", "frechet", "mean", "std"]

    for i in range(len(pt_files)):
        for pt_file in fu.list_directory_files(pt_path, ".csv", pt_files[i]):
            # Combining the two filenames for the aligned output
            output_filename = dt_file[i][:dt_file.index(".csv")] + pt_file[:pt_file.index(".csv")]
            output_dir_filename = output_directory + output_filename  + ".csv"

            # Analysis file for different gap values initialization
            file_writer, writer = cu.get_writer(output_dir_filename, ",", 'w')
            writer.writerow(headers)

            # DT and PT traces in dict
            dt_trace = pd.read_csv(dt_path + dt_file[i])
            pt_trace = pd.read_csv(pt_path + pt_file)

            # You could try with different values of gap
            for gap in np.arange(-0.25, 0.05, 0.05):
                output_dir_filename_gap = output_directory + output_filename + "-" + "{:.2f}".format(gap) + ".csv"

                # --- CALCULATE ALIGNMENT - MAIN ALGORITHM ---
                start_time = time.time()

                ndw = NeedlemanWunschTolerance(dt_trace.to_dict('records'),
                                               pt_trace.to_dict('records'),
                                               Lift(),
                                               initiate_gap=gap)
                alignment_df = ndw.calculate_alignment()

                print(f"--- Gap {gap} : {(time.time() - start_time):2f} seconds ---")

                alignment_df.to_csv(output_dir_filename_gap, index=False, encoding='utf-8', sep=',')

                # --- GRAPHIC GENERATION ---
                generate_alignment_graphic(alignment_df, dt_trace, pt_trace, param_interest, timestamp_label,
                                           output_path=output_dir_filename_gap)

                # --- DISTANCE ANALYSIS ---
                percentage_matched, frechet, euclidean, std = measure_distance(alignment_df, dt_trace, pt_trace,
                                                                               [param_interest])
                writer.writerow([gap, percentage_matched, frechet, euclidean, std])

            # --- GAP AND PERCENTAGE MATCHED COMPARISON ---
            file_writer.close()
            generate_statistical_info_graphic(output_dir_filename)




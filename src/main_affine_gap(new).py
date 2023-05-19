import argparse
import os
import time

import numpy as np
import pandas as pd
import yaml

import util.file_util as fu
from algorithm.needleman_wunsch_affine_gap import NeedlemanWunschAffineGap
from analysis.alignment_lca import AlignmentLCA
from result_analysis.alignment_graphic import generate_alignment_graphic
from systems_config.lift import Lift
from systems_config.system import SystemBase
from util.float_util import get_input_values_list

MAD = 'mad'
LOW = 'low'
INIT_GAP = 'init_gap'
CONT_GAP = 'cont_gap'

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", help="It processes the alignment and generates figures as image files")
    args = parser.parse_args()

    current_directory = os.path.join(os.getcwd(), "")

    # Read the YAML file
    with open(current_directory + 'config/lift.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # FILE PATHS
    input_directory = current_directory + config['paths']['input']['main']
    output_directory = current_directory + config['paths']['output']

    # DIGITAL TWIN
    dt_path = input_directory + config['paths']['input']['dt']
    dt_file = config['paths']['input']['dt_files']

    # PHYSICAL TWIN
    pt_path = input_directory + config['paths']['input']['pt']
    pt_files = config['paths']['input']['pt_files']

    # ANALYSIS PARAMETERS
    timestamp_label = config['labels']['timestamp_label']
    param_interest = config['labels']['param_interest']

    # INPUT PARAMETERS
    ranges = config['ranges']

    # Calculate Maximum Acceptable Distance (MAD)
    max_acceptable_dist = np.arange(
        ranges['mad']['start'],
        ranges['mad']['end'],
        ranges['mad']['step']
    )

    # Calculate Weight for Low complexity areas
    low = np.arange(
        ranges['low']['start'],
        ranges['low']['end'],
        ranges['low']['step']
    )

    # Calculate Weights for Affine Gap
    init_gap = np.arange(
        ranges['init_gap']['start'],
        ranges['init_gap']['end'],
        ranges['init_gap']['step']
    )
    factor = 11
    continue_gap = init_gap / factor

    input_values = get_input_values_list(max_acceptable_dist, low, init_gap, continue_gap, factor=factor)
    methods = fu.get_property_methods(AlignmentLCA)

    # Iterate over Physical Twin Files against Digital Twins'
    for i in range(len(pt_files)):
        for pt_file in fu.list_directory_files(pt_path, ".csv", pt_files[i]):
            # Unique filename combining both in format : <fileAfileB>
            output_filename = os.path.splitext(dt_file[i])[0] + os.path.splitext(pt_file)[0]
            # Output directory combined with filename and extension : path/to/output/fileAfileB.csv
            output_dir_filename = f"{output_directory}{output_filename}.csv"

            # DT and PT traces in dict
            dt_trace = pd.read_csv(dt_path + dt_file[i])
            pt_trace = pd.read_csv(pt_path + pt_file)

            statistical_results_df = pd.DataFrame()
            for inputs in input_values:
                input_dict = {
                    MAD: {
                        param_interest: inputs[0],
                        timestamp_label: inputs[0]
                    },
                    LOW: inputs[1],
                    INIT_GAP: inputs[2],
                    CONT_GAP: inputs[3]
                }

                config_output_dir_filename = f"{output_directory}{output_filename}-({input_dict[INIT_GAP]:.2f}," \
                                             f"{input_dict[CONT_GAP]:.2f})" \
                                             f"-{input_dict[LOW]}" \
                                             f"-{input_dict[MAD][param_interest]}.csv"

                # --- CALCULATE ALIGNMENT - MAIN ALGORITHM ---
                if config['system'] == 'Lift':
                    cps = Lift()
                else:
                    cps = SystemBase()

                start_time = time.time()
                ndw = NeedlemanWunschAffineGap(dt_trace.to_dict('records'),
                                               pt_trace.to_dict('records'),
                                               cps,
                                               initiate_gap=input_dict[INIT_GAP],
                                               continue_gap=input_dict[CONT_GAP],
                                               low=input_dict[LOW],
                                               mad=input_dict[MAD])
                alignment_df = ndw.calculate_alignment()

                print(f"--- SCENARIO: {output_filename} ---")
                print(f"--- Init gap {input_dict[INIT_GAP]:.2f}, Continue gap {input_dict[CONT_GAP]:.2f} : "
                      f"{(time.time() - start_time):.2f} seconds ---")

                alignment_df.to_csv(config_output_dir_filename, index=False, encoding='utf-8', sep=',')

                if args.figures:
                    # --- GRAPHIC GENERATION ---
                    generate_alignment_graphic(alignment_df, dt_trace, pt_trace, param_interest, timestamp_label,
                                               output_path=config_output_dir_filename,
                                               mad=input_dict[MAD][param_interest],
                                               open_gap=input_dict[INIT_GAP], continue_gap=input_dict[CONT_GAP])

                # --- DISTANCE ANALYSIS ---
                alignment_results = AlignmentLCA(alignment_df, dt_trace, pt_trace, cps, [param_interest])
                statistical_values = fu.get_property_values(alignment_results, methods)
                concatenated_dict = {**fu.flatten_dictionary(input_dict),
                                     **fu.flatten_dictionary(statistical_values)}

                statistical_results_df = pd.concat([statistical_results_df,
                                                    pd.DataFrame.from_records([concatenated_dict])], ignore_index=True)
            statistical_results_df.to_csv(output_dir_filename, index=False)

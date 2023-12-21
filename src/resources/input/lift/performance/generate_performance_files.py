import os

import numpy as np
import pandas as pd


def compose_max_file(scenario_filepath: str, max_repetitions: float) -> pd.DataFrame:
    original_df = pd.read_csv(scenario_filepath)
    original_info = original_df.to_numpy(dtype=str)
    new_info = original_info.copy()
    original_rows = len(original_info)
    increment_number = max_repetitions // original_rows + \
                       1 if max_repetitions % original_rows > 0 else 0

    previous = original_rows - 1
    for i in range(2, increment_number):
        for j, row in enumerate(original_info):
            new_row = row.copy()
            new_row[0] = str(float(new_info[previous][0]) + float(row[0]))
            previous += 1
            new_info = np.append(new_info, new_row.reshape(1, 4), axis=0)

    new_df = pd.DataFrame(new_info)
    new_df.columns = original_df.columns
    return new_df


def main():
    # input_files = ['Bajada_4_3_2_1_0_1_2_3_4-events.csv', 'Bajada_4_3_2_1_0_1_2_3_4_01-events.csv']
    input_files = ['dt-events.csv', 'pt-events.csv']
    base_output_path = './output_directory/'
    os.makedirs(base_output_path, exist_ok=True)

    total_rows = 10000
    increment = 500

    first = [i for i in range(100, 501, 100)]
    medium = [j for j in range(1000, 5001, 500)]
    later = [k for k in range(6000, 10001, 1000)]

    for file in input_files:
        max_df = compose_max_file(file, total_rows)
        for i in (first + medium + later):
            max_df.head(i).to_csv(f"{base_output_path}{file.split('.')[0]}_subset_{i}.csv",
                                  index=False)


if __name__ == "__main__":
    main()

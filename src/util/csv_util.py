import csv


def get_reader(filepath: str, delim: str):
    """It returns the file handler and a csv reader using the input delimiter."""
    file = open(filepath, 'r', newline='')
    reader = csv.reader(file, delimiter=delim)
    return file, reader


def get_writer(filepath: str, delim: str, write_mode: str):
    """It returns the file handler and a csv writer using the input delimiter."""
    file = open(filepath, write_mode, newline='')
    writer = csv.writer(file, delimiter=delim, dialect='excel')
    return file, writer


def process_timestamp(path: str, delim: str, position: int):
    """It returns a new csv file with time values in seconds. Input format is HH:MM:SS."""
    file_r, reader = get_reader(path, delim)
    input_matrix = list(reader)
    output = [input_matrix[1]]
    for row in input_matrix[2:]:
        time_values = row[position].split(":")
        relative_timestamp = sum(
            [float(value) * pow(60, len(time_values) - (index + 1)) for index, value in enumerate(time_values)])
        new_row = [row[0:position], relative_timestamp]
        new_row.extend(row[position + 1:])
        output.append(new_row)

    file_r.close()

    file_w, writer = get_writer(path, delim, 'w')
    writer.writerows(output)
    file_w.close()

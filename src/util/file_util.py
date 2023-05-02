import os


def list_directory_files(dir: str, extension: str):
    """It returns a list with all the files of a given extension."""
    result = []
    for file in os.listdir(dir):
        if file.endswith(extension):
            result.append(file)
    return result


def list_directory_files(dir: str, extension: str, pattern: str):
    """It returns a list with all the files of a given extension and starts with pattern."""
    result = []
    for file in os.listdir(dir):
        if file.endswith(extension) and file.startswith(pattern):
            result.append(file)
    return result


def replace_str(input_path: str, out_path: str, pattern: str, new_pattern: str):
    """Replaces a string in a file."""
    output_file = open(out_path, 'w')
    with open(input_path, 'r') as input_file:
        for line in input_file:
            output_file.write(line.replace(pattern, new_pattern))
    output_file.close()

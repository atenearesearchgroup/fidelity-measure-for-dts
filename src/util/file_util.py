import inspect
import os


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


def flatten_dictionary(dictionary, parent_key='', sep='_'):
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dictionary(value, new_key, sep))
        else:
            flattened_dict[new_key] = value
    return flattened_dict


def get_property_methods(cls):
    properties = []
    for name, method in inspect.getmembers(cls):
        if isinstance(method, property):
            properties.append(name)
    return properties


def get_property_values(obj, methods):
    values = {}
    for name in methods:
        values[name] = getattr(obj, name)
    return values

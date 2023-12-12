import inspect
import os


def list_directory_files(dir: str, extension: str, pattern: str):
    """It returns a list with all the files of a given extension and starts with pattern."""
    result = []
    for file in os.listdir(dir):
        if file.endswith(extension) and file.startswith(pattern):
            result.append(file)
    return result


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


def generate_sublist(label_params: list, include_params: list):
    result = []
    for params in include_params:
        result.extend(label_params[params[0]:params[1] + 1])

    return result


def generate_filename(parameter_values):
    """
        Generate a filename based on a set of parameter values.

        :param parameter_values: A dictionary containing parameter names as
        keys and their values.

        :return str: The generated filename.
    """
    param_strings = []
    for key, value in parameter_values.items():
        if isinstance(value, (int, float)):
            param_strings.append(f"{key[:2]}_{value:.2f}")
        elif isinstance(value, dict):
            param_strings.append(f"{key[:3]}_{list(value.values())[0]}")
        else:
            param_strings.append(f"{key[:2]}_{value}")

    return "-".join(param_strings)

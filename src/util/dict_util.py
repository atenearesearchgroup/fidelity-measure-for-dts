import numpy as np


def nested_get(dic, keys):
    for key in keys:
        dic = dic[key]
    return dic


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def get_range(dic):
    if isinstance(dic, dict):
        return np.arange(
            dic['start'],
            dic['end'],
            dic['step']
        )
    else:
        return [dic]


def tuple_to_dict(labels: list, current_config: tuple) -> dict:
    result = {}
    for index, label in enumerate(labels):
        nested_set(result, label.split('-'), current_config[index])
    return result


def dict_to_str(parameter_values):
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
            param_strings.append(f"{key[:2]}_{list(value.values())[0]}")
        else:
            param_strings.append(f"{key[:2]}_{value}")

    return "-".join(param_strings)

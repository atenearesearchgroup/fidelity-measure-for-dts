import itertools


def max_tolerance(v1: float, v2: float, v3: float, equals_value: float, tolerance: float = 0.0001) -> (float, int):
    """Comparison of three floats considering a certain tolerance.
        Returns
        --------
        Maximum value and its position
    """
    if v1 >= (v3 - tolerance):
        if v1 >= (v2 - tolerance):
            max_value = v1
            max_index = 3 if equals_value > 0 else 2
        else:
            max_value = v2
            max_index = 1
    elif v3 >= (v2 - tolerance):
        max_value = v3
        max_index = 0
    else:
        max_value = v2
        max_index = 1
    return max_value, max_index


def get_input_values_list(*args):
    combinations = []
    for elements in itertools.product(*args):
        combinations.append(elements)
    return combinations

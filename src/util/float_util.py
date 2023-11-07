import itertools


def max_tolerance(v1: float, v2: float, v3: float, equals_value: float,
                  tolerance: float = 0.0001) -> (float, int):
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


def min_tolerance(v1: float, v2: float, v3: float,
                  tolerance: float = 0.0001) -> (float, int):
    """Comparison of three floats considering a certain tolerance.
        Returns
        --------
        Min value and its position
    """
    if v1 <= (v3 - tolerance):
        if v1 <= (v2 - tolerance):
            min_value = v1
            min_index = 1
        else:
            min_value = v2
            min_index = 2
    elif v3 <= (v2 - tolerance):
        min_value = v3
        min_index = 3
    else:
        min_value = v2
        min_index = 3
    return min_value, min_index


def get_input_values_list(*args):
    combinations = []
    for elements in itertools.product(*args):
        combinations.append(elements)
    return combinations

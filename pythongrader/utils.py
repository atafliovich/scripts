"""Some useful functions commonly used in testing student code."""

from typing import Dict, List
from .config import EPSILON


def float_eq(x: float, y: float) -> bool:
    """To be used as comparator for floats."""

    return abs(x - y) < EPSILON


def same_lists(xlist: list, ylist: list) -> bool:
    """Return True if and only if xlist and ylist are equal lists,
    regardless of the order in which elements occur.
    """

    return len(xlist) == len(ylist) and all(x in ylist for x in xlist)


def same_key_to_list_dicts(key_to_list1: Dict[str, List[str]],
                           key_to_list2: Dict[str, List[str]]) -> bool:
    """Return True if and only if key_to_list1 and key_to_list2 are equal
    dictionaries, regardless of the order in which elements occur in
    the dictionaries' values.
    """

    if key_to_list1.keys() != key_to_list2.keys():
        return False

    for key in key_to_list1:
        if not same_lists(key_to_list1[key], key_to_list2[key]):
            return False

    return True


def invert_dictionary(key_to_values: Dict[object, list]) -> dict:
    """Return key_to_values inverted.
    """

    value_to_key = {}

    for (key, value) in key_to_values.items():
        if value not in value_to_key:
            value_to_key[value] = []
        value_to_key[value].append(key)

    return value_to_key


if __name__ == '__main__':
    import doctest
    doctest.testmod()

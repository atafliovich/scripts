"""Some useful functions commonly used in testing student code."""

from .config import EPSILON


def float_eq(x: float, y: float) -> bool:
    """To be used as comparator for floats."""

    return abs(x - y) < EPSILON


def same_lists(xlist: list, ylist: list) -> bool:
    """Return True if and only if xlist and ylist are equal lists,
    regardless of the order in which elements occur.

    >>> same_lists([], [])
    True
    >>> same_lists([42], [42])
    True
    >>> same_lists([42], [24])
    False
    >>> same_lists([1, 2, 3, 4, 5], [1, 3, 2, 5, 4])
    True

    """

    return len(xlist) == len(ylist) and all(x in ylist for x in xlist)


def same_lists_of_lists(xlist: list, ylist: list) -> bool:
    """Return True if and only if xlist and ylist are equal lists or
    lists, regardless of the order in which elements in sublists occur.

    >>> same_lists_of_lists([[], [42], [1, 2, 3, 4, 5]],
    ...                     [[], [42], [1, 3, 2, 5, 4]])
    True
    """

    return len(xlist) == len(ylist) and all(map(lambda t: same_lists(*t),
                                                zip(xlist, ylist)))


def same_key_to_list_dicts(key_to_list1: dict[str, list[str]],
                           key_to_list2: dict[str, list[str]]) -> bool:
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


def invert_dictionary(key_to_values: dict[object, list]) -> dict:
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

"""Settings for testing this assignment."""

# The name of the student module that we are testing.
MODULENAME = 'bridge_functions'

# The name of the student file that we are testing.
FILENAME = 'bridge_functions.py'

# Where is pyta?
PYTA_LOCATION = '/home/anya/a08/assignments/a2/starter/pyta'

# Where is the pyta config file?
PYTA_CONFIG_FILE = '/home/anya/a08/assignments/a2/starter/pyta/a2_pyta.txt'

# Where to put the output of pyta.
PYTA_OUT_FILENAME = 'pyta_output.txt'

# Timeout per test method
TIMEOUT = 2

# The functions that need to be tested. Used to generate a skeleton
# unittest test suite.
FUNC_TO_ANNOTATIONS = {
    'get_bridge': ([list[list], int], list),
    'get_average_bci': ([list[list], int], float),
    'get_total_length_on_hwy': ([list[list], str], float),
    'get_distance_between': ([list, list], float),
    'get_closest_bridge': ([list[list], int], int),
    'get_bridges_in_radius': ([list[list], float, float, float], list[int]),
    'get_bridges_with_bci_below': ([list[list], list[int], float], list[int]),
    'get_bridges_containing': ([list[list], str], list[int]),
    'assign_inspectors': (
        [list[list], list[list[float]], int], list[list[int]]),
    'inspect_bridges': ([list[list], list[int], str, float], None),
    'add_rehab': ([list[list], int, str, bool], None),
    'format_data': ([list[list[str]]], None)
}

FUNCTIONS = FUNC_TO_ANNOTATIONS.keys()

# Testing docstrings:

# will not check presence of examples in these
FUNCTIONS_WITH_IO = ()

# Valid command words of a docstring.
COMMAND_WORDS = {'return', 'update', 'modify', 'add', 'change'}

# Is the use of third person command words allowed in docstrings?
# E.g., "returns" instead of "return".
ALLOW_THIRD_PERSON = True

# Min number of examples required.
NUM_EXAMPLES = 2

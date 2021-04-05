""" Settings for testing this assignment.
"""

# The name of the student module that we are testing.
MODULENAME = 'puzzler_functions'

# The functions that need to be tested. Used to generate a skeleton
# unittest test suite.
FUNC_TO_ANNOTATIONS = {
    'is_win': ([str, str], bool),
    'is_game_over': ([str, str, str], bool),
    'erase': ([str, int], str)
}

FUNCTIONS = FUNC_TO_ANNOTATIONS.keys()

# Testing docstrings:

# will not check presence of examples in these
FUNCTIONS_WITH_IO = ()

# Valid command words of a docstring.
COMMAND_WORDS = {'return'}  # , 'update', 'modify', 'add', 'change'

# Is the use of third person command words allowed in docstrings?
# E.g., "returns" instead of "return".
ALLOW_THIRD_PERSON = False

# Min number of examples required.
NUM_EXAMPLES = 2

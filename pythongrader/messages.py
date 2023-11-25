""" Various message formats used by the grader.
"""

### Correctness Test Failure/Error Messages ###
FAILURE_MESSAGE = '''
When we called {}, we expected to get:
{}
but your code produced this:
{}'''

FAILURE_MESSAGE_MUTATION = '''
When we called {}, we expected argument {} to become:
{}
but your code produced this:
{}'''

FAILURE_MESSAGE_NO_MUTATION = '''
The call {} should not modify its arguments.
The new values were: {}.
'''

FAILURE_MESSAGE_NO_MUTATION_INDEX = '''
The call {} should not modify its argument at index {}.
The new value was: {}.
'''

FAILURE_MESSAGE_CONSTANTS = '''
This set of tests checks whether you used the constants provided
and did not hard-code their values. We changed the values of your
constants to these:
{}
Then, when we called {}, we expected this:
{}
but your code returned this:
{}'''


ERROR_MESSAGE = '''
The call {} caused an error:
{}'''


ERROR_MESSAGE_CONSTANTS = '''
This set of tests checks whether you used the constants provided
and did not hard-code their values. We changed the values of your
constants to these:
{}
Then, when we called {}, the call caused an error:
{}'''


COMPARE_MESSAGE = '''
When we tried to compare the result of the call {}
with {},
we got an error: {}'''


COMPARE_MESSAGE_CONSTANTS = '''
This set of tests checks whether you used the constants provided
and did not hard-code their values. We changed the values of your
constants to these:
{}
Then when we tried to compare the result of the call {}
with {},
we got an error: {}'''


### Docstrings Test Failure/Error Messages ###

EXISTS_FAILURE_MESSAGE = '''
{}'s docstring could not be found
'''
FIRST_WORD_FAILURE_MESSAGE = '''
{}'s docstring should be phrased as a command: eg: "Return/Modify/..."'''

COMMAND_WORD_FAILURE_MESSAGE = '''
{}'s docstring should be phrased to contain the following commands: {}'''

PARAM_FAILURE_MESSAGE = '''
{}'s docstring does not list all of its parameters by name.
Missing : {}
'''

EXAMPLE_FAILURE_MESSAGE = '''
{}'s docstring does not contain enough examples ({})
{} example(s) found.
'''

PARAM_ANNOTATION_FAILURE_MESSAGE = '''
{} expected to have the following parameter type annotations:
 {}
but its annotations are actually:
 {}
'''

RETURN_ANNOTATION_FAILURE_MESSAGE = '''
{} expected to have the following return type annotation:
 {}
but its annotation is actually:
 {}
'''


### Student unittests Test Failure/Error Messages ###

TESTER_FAILURE_FALSE_NEGATIVE_MESSAGE = '''
When we ran the tester file on the following implementation,
it did not detect the bug(s):
{}
'''

TESTER_FAILURE_FALSE_POSITIVE_MESSAGE = '''
When we ran the tester file on the correct implementation,
it failed.
'''

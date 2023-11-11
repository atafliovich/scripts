"""Set up a skeleton unittest test suite."""

import argparse
import importlib
import os

# Generate a tester for doctests?
TEST_DOCTEST = True

# Generate a tester for docstrings?
TEST_DOCSTRINGS = True

# Generate a tester for constants?
TEST_CONSTANTS = True


CONTENTS = '''""" Test cases for function {functionname}."""

import sys
import unittest
import timeout_decorator

from privateconfig import SCRIPTS_DIR
from config import MODULENAME, TIMEOUT
sys.path.append(SCRIPTS_DIR)           # noqa
from grader.test_base import TestBase  # noqa

try:
    import {modulename}
except ImportError:
    pass


class {testclassname}(TestBase):
    """Test cases for function {modulename}.{functionname}."""

    def _get_module_name(self):
        return MODULENAME

    def setUp(self):
        super().setUp()
        # may want to reset constants, etc. here

    def test_00_empty(self):
        self._test(['', ''], True)

    @timeout_decorator.timeout(TIMEOUT)
    def _test(self, args, expected):
        (status, msg) = self._check({modulename}.{functionname},
                                    args, expected)
        if not status:
            self.fail(msg)


if __name__ == '__main__':
    unittest.main(exit=False)
'''

CONTENTS_DOCTEST = '''""" Tester for function doctests."""

import sys
import unittest

from privateconfig import SCRIPTS_DIR
from config import FUNCTIONS, MODULENAME
sys.path.append(SCRIPTS_DIR)  # noqa
import grader.test_doctest    # noqa

try:
    import {modulename}
except ImportError:
    pass


class TestDoctest(grader.test_doctest.TestDoctestBase):
    """Dummy child."""

    def _get_module_name(self):
        return MODULENAME


grader.test_doctest.auto_make_test_from_functions(
    TestDoctest, FUNCTIONS, {modulename})


if __name__ == '__main__':
    unittest.main()
'''

CONTENTS_DOCSTRINGS = '''""" Test cases for docstrings."""

import sys
import unittest
from privateconfig import SCRIPTS_DIR
from config import (ALLOW_THIRD_PERSON, COMMAND_WORDS, FUNCTIONS,
                    FUNC_TO_ANNOTATIONS, FUNCTIONS_WITH_IO,
                    MODULENAME, NUM_EXAMPLES)
sys.path.append(SCRIPTS_DIR)         # noqa
from grader import test_docstrings   # noqa


try:
    import {modulename}
except ImportError:
    pass


# Do NOT call new tests "test_*", because unittest will collect and run them!
TESTS = [test_docstrings.TestDocstringsBase.exists_test,
         test_docstrings.TestDocstringsBase.command_word_test,
         test_docstrings.TestDocstringsBase.params_test,
         test_docstrings.TestDocstringsBase.num_examples_test,
         test_docstrings.TestDocstringsBase.annotations_test]


SETTINGS = {{'module': {modulename},
             'func_to_annotations': FUNC_TO_ANNOTATIONS,
             'functions_with_io': FUNCTIONS_WITH_IO,
             'command_words': COMMAND_WORDS,
             'num_examples': NUM_EXAMPLES,
             'allow_third_person': ALLOW_THIRD_PERSON}}


class TestDocstrings(test_docstrings.TestDocstringsBase):
    """Dummy child."""

    def _get_module_name(self):
        return MODULENAME


test_docstrings.auto_make_tests_from_functions(
    TestDocstrings, FUNCTIONS, TESTS, SETTINGS)


if __name__ == '__main__':
    unittest.main()
'''

CONTENTS_CONSTANTS = '''""" Test cases for testing student use of constants."""

import sys
import unittest
import timeout_decorator

from privateconfig import SCRIPTS_DIR
from config import MODULENAME, TIMEOUT
sys.path.append(SCRIPTS_DIR)  # noqa
from grader.test_constants import TestConstantsBase   # NOQA: E402


try:
    import {modulename}
except ImportError:
    pass


class TestConstants(TestConstantsBase):
    """Check use of constants in {modulename}."""

    def setUp(self):
        self.constant_to_value = {{
            # TODO: set new values for constants
        }}

    def _get_module_name(self):
        return MODULENAME

    # TODO: fill in all implementations below
    {constants_tests}

    @timeout_decorator.timeout(TIMEOUT)
    def _test(self, func, args, expected):
        (status, msg) = self._check_use_of_constants(func, args, expected,
                                                     self.constant_to_value)
        if not status:
            self.fail(msg)


if __name__ == '__main__':
    unittest.main(exit=False)
'''


def make_test_file(func_name: str, test_num: int, module_name: str,
                   directory: str = '.') -> None:
    """Write a skeleton unittest file number test_num to test function
    func_name in directory.

    module_name: the name of the student module we are testing.
    directory: directory in which to write the test files.
    """

    test_class_name = 'Test{}'.format(
        ''.join(word.title() for word in func_name.split('_')))

    contents = CONTENTS.format(functionname=func_name,
                               modulename=module_name,
                               testclassname=test_class_name)
    _make_file(func_name, test_num, directory, contents)


def make_doctest_file(test_num: int, module_name: str, directory:
                      str = '.') -> None:
    """Write a doctest file (a tester for students' doctests) number
    test_num in directory.

    module_name: the name of the student module we are testing.
    directory: directory in which to write the test files.

    """

    contents = CONTENTS_DOCTEST.format(modulename=module_name)
    _make_file('doctest', test_num, directory, contents)


def make_docstrings_file(test_num: int, module_name: str,
                         func_to_annotations: dict[str, tuple[list[str], str]],
                         directory: str = '.') -> None:
    """Write a docstrings test file (a tester for students' docstrings)
    number test_num in directory.

    module_name: the name of the student module we are testing.
    directory: directory in which to write the test files.
    func_to_annotations: maps each required function name to its
      required annotations (List[input-types], output-type)

    """

    contents = CONTENTS_DOCSTRINGS.format(
        modulename=module_name,
        func_to_annotations=func_to_annotations)
    _make_file('docstrings', test_num, directory, contents)


def make_test_constants_file(test_num: int, module_name: str,
                             functions: list[str],
                             directory: str = '.') -> None:
    """Write a starter for constants test file (a tester for students
    using constants rather than their values in the starter code)
    number test_num in directory.

    module_name: the name of the student module we are testing.
    functions: list of function names.
    directory: directory in which to write the test files.

    """

    constants_tests = _make_constants_tests(module_name, functions)
    contents = CONTENTS_CONSTANTS.format(modulename=module_name,
                                         constants_tests=constants_tests)
    _make_file('constants', test_num, directory, contents)


def _make_file(name_part: str, test_num: int, directory: str = '.',
               contents: str = '') -> None:

    file_name = os.path.join(
        directory,
        f'test_{str(test_num).zfill(2)}_{name_part}.py')

    with open(file_name, 'w', encoding='utf-8') as outfile:
        outfile.write(contents)


def _make_constants_tests(module_name: str, functions: list[str]) -> str:

    content = ''

    teststub = '''

    def test_{num}_{func}(self):
        self._test({modulename}.{func}, [], True)'''

    for num, func in enumerate(functions):
        content += teststub.format(num=str(num).zfill(2),
                                   func=func,
                                   modulename=module_name)
    return content


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description=('Set up a skeleton unittest test suite '
                     '(for an assignment).'))

    PARSER.add_argument('--config', default='config.py',
                        help='Full path of configuration file.')
    PARSER.add_argument('--directory', default='.',
                        help='Directory in which to create test files.')

    ARGS = PARSER.parse_args()

    NAME = os.path.split(ARGS.config)[1]
    CONFIG = importlib.import_module(NAME.split('.py')[0])

    for i, name in enumerate(CONFIG.FUNCTIONS):
        make_test_file(name, i, CONFIG.MODULENAME, ARGS.directory)

    file_num = len(CONFIG.FUNCTIONS)
    if TEST_DOCTEST:
        make_doctest_file(file_num, CONFIG.MODULENAME)
        file_num += 1
    if TEST_DOCSTRINGS:
        make_docstrings_file(file_num, CONFIG.MODULENAME,
                             CONFIG.FUNC_TO_ANNOTATIONS,
                             ARGS.directory)
        file_num += 1
    if TEST_CONSTANTS:
        make_test_constants_file(file_num, CONFIG.MODULENAME,
                                 CONFIG.FUNCTIONS, ARGS.directory)

"""Base for unit tests. Do not modify: extend TestBase with your own
test classes. See below for possible methods to override.

"""

import copy
import importlib
import operator
import sys
from typing import Callable, Dict, Tuple
import unittest

from .messages import (COMPARE_MESSAGE, FAILURE_MESSAGE,
                       FAILURE_MESSAGE_MUTATION, ERROR_MESSAGE,
                       FAILURE_MESSAGE_NO_MUTATION)


class TestBase(unittest.TestCase):
    """To be subclassed in the test classes."""

    # override if needed, but call super.setUp()
    def setUp(self):
        importlib.reload(sys.modules[self._get_module_name()])

    def _get_module_name(self):
        raise Exception("Override me.")

    # Most likely you can use this method as is. If not, look at
    # helpers below to override.
    def _check(self, func: Callable, args: list, expected: object,
               comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Check if func(args) returns a result R such that
        comparator(expected, R) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        """

        try:
            returned = func(*args)
        except Exception as exn:
            return (False, _make_error_msg(func, args, exn))

        try:
            as_expected = comparator(expected, returned)
        except Exception as exn:
            return (False, _make_compare_msg(func, args, expected, exn))

        if as_expected:
            return (True, '')

        return (False, _make_failure_msg(func, args, expected, returned))

    # Most likely you can use this method as is. If not, look at
    # helpers below to override.
    def _check_mutated(self, func: Callable, args: list, mutated_index: int,
                       expected: object,
                       comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Check if function func, when called with arguments args, mutates
        the argument at index mutated_index in args, such that after
        the call the value of this argument is arg such that
        comparator(expected, arg) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        """

        args_copy = copy.deepcopy(args)
        try:
            func(*args)
        except Exception as exn:
            return (False, _make_error_msg(func, args_copy, exn))

        try:
            as_expected = comparator(expected, args[mutated_index])
        except Exception as exn:
            return (False, _make_compare_msg(func, args_copy, expected, exn))

        if as_expected:
            return (True, '')

        return (False,
                _make_failure_mutation_msg(func, args_copy, mutated_index,
                                           args[mutated_index], expected))

    # Most likely you can use this method as is. If not, look at
    # helpers below to override.
    def _check_not_mutated(self, func: Callable, args: list,
                           comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Check that function func, when called with arguments args, does
        not mutate the arguments. If args_mut are the args after the call,
        comparator(args, args_mut) must be True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        """

        args_mut = copy.deepcopy(args)
        try:
            func(*args_mut)
        except Exception as exn:
            return (False, _make_error_msg(func, args, exn))

        try:
            as_expected = comparator(args, args_mut)
        except Exception as exn:
            return (False, _make_compare_msg(func, args, args_mut, exn))

        if as_expected:
            return (True, '')

        return (False, _make_failure_no_mutation_msg(func, args, args_mut))

    # override if needed
    def _check_no_mocks(self, func: Callable, args: list, expected: object,
                        comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Check if func(args) returns a result R such that comparator(R,
        expected) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        """

        return self._check(func, args, expected, comparator)

    # override if needed
    def _check_with_mocks(self, func: Callable, args: list, expected: object,
                          _mock_specs: Dict[str, Callable],
                          comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Mock functions in the student module according to _mock_specs. Then
        check if func(args) returns R such that comparator(R,
        expected) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        _mock_specs maps a name of the function to be mocked to the
                    corresponding mock function.

        The default comparator is the function that corresponds to
        operator ==.

        """

        self._mock(_mock_specs)
        return self._check(func, args, expected, comparator)

    def _check_no_mocks_mutation(self, func: Callable, args: list,
                                 mutated_index: int, expected: object,
                                 comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Check if func(args) mutates the argument at index mutated_index in
        args, such that after the call the value of this argument is
        arg such that comparator(expected, arg) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        """

        return self._check_mutated(func, args, mutated_index,
                                   expected, comparator)

    # override if needed
    def _check_with_mocks_mutation(self, func: Callable, args: list,
                                   mutated_index: int, expected: object,
                                   _mock_specs: Dict[str, Callable],
                                   comparator: Callable = operator.eq) -> Tuple[bool, str]:
        """Mock functions in the student module according to _mock_specs.
        Then check if function func(args) mutates the argument at
        index mutated_index in args, such that after the call the
        value of this argument is arg such that comparator(expected,
        arg) is True.

        Return (True, '') if the check succeeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        _mock_specs maps a name of the function to be mocked to the
                    corresponding mock function.

        """

        self._mock(_mock_specs)
        return self._check_mutated(func, args, mutated_index,
                                   expected, comparator)

    def _mock(self, fnames_to_mocks: Dict[str, Callable]):
        """Mock each function in fnames_to_mocks with its corresponding mock
        function in the student module.

        """

        test_module = sys.modules[MODULENAME]
        for fname, mock in fnames_to_mocks.items():
            setattr(test_module, fname, mock)


def _make_call_string(func: callable, args: list) -> str:
    """Return a string that represents the call func(args)."""

    return "{}({})".format(func.__name__, ", ".join(map(repr, args)))


def _make_failure_msg(func: callable, args: list,
                      expected: object, actual: object) -> str:
    """Return a failure message: func(args) failed."""

    return FAILURE_MESSAGE.format(_make_call_string(func, args),
                                  expected, actual)


def _make_failure_mutation_msg(func: callable, args: list, mutated_index: int,
                               actual: object, expected: object) -> str:
    """Return a failure message: func(args) failed to mutate arg at
    mutated_index.

    """
    return FAILURE_MESSAGE_MUTATION.format(_make_call_string(func, args),
                                           mutated_index, expected, actual)


def _make_failure_no_mutation_msg(func: callable, args: list, args_mut: list) -> str:
    """Return a failure message: func(args) should not mutate, new values are args_mut."""

    return FAILURE_MESSAGE_NO_MUTATION.format(_make_call_string(func, args), args_mut)


def _make_error_msg(func: callable, args: list,
                    error: Exception) -> str:
    """Return an error message: func(args) raised an error."""

    return ERROR_MESSAGE.format(_make_call_string(func, args), error)


def _make_compare_msg(func: callable, args: list,
                      expected: object, error: Exception) -> str:
    """Return a comparison error message: comparing func(args) and
    expected raised an error."""

    return COMPARE_MESSAGE.format(_make_call_string(func, args),
                                  expected, error)

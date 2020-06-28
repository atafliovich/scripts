"""Base tester for students' use of constants (hardcoding values
instead of using specified constants) in their solutions.

"""

import operator
import sys
from typing import Callable, Dict, Tuple

from .messages import (COMPARE_MESSAGE_CONSTANTS,
                       ERROR_MESSAGE_CONSTANTS,
                       FAILURE_MESSAGE_CONSTANTS)
from .test_base import _make_call_string, TestBase


class TestConstantsBase(TestBase):
    """Base class for testing that students use constants rather than
    their values.

    """

    def _check_use_of_constants(
            self, func: Callable, args: list, expected: object,
            _constant_to_value: Dict[str, object], modulename: str,
            comparator: callable = operator.eq) -> Tuple[bool, str]:
        """Set values of constants in the student module according to
        _constant_to_value. Then check if func(args) returns R such
        that comparator(expected, R) is True.

        Return (True, '') if the check suceeds.
        Return (False, error-or-failure-message) if anything goes wrong.

        The default comparator is the function that corresponds to
        operator ==.

        _constant_to_value maps names of constants in the student
          module to their values.

        """

        self._set_constants(_constant_to_value, modulename)

        try:
            returned = func(*args)
        except Exception as exn:
            return (False, _make_error_constants_msg(
                func, args, _constant_to_value, exn))

        try:
            as_expected = comparator(expected, returned)
        except Exception as exn:
            return (False, _make_compare_constants_msg(
                func, args, expected, _constant_to_value, exn))

        if as_expected:
            return (True, '')

        return (False, _make_failure_constants_msg(
            func, args, expected, returned, _constant_to_value))

    def _set_constants(self, _constant_to_value: Dict[str, object], modulename: str) -> None:
        """Set the values of constants in the student module according to
        _constant_to_value.

        _constant_to_value maps names of constants in the student
          module to their values.

        """

        test_module = sys.modules[modulename]
        for constant, value in _constant_to_value.items():
            setattr(test_module, constant, value)


def _make_error_constants_msg(func: callable, args: list,
                              _constant_to_value: Dict[str, object],
                              error: Exception) -> str:
    """Return an error message about the use of constants: func(args)
    raised an error after setting constants to values in
    _constant_to_value.

    """

    return ERROR_MESSAGE_CONSTANTS.format(
        _make_constants_and_values_msg(_constant_to_value),
        _make_call_string(func, args), error)


def _make_failure_constants_msg(func: callable, args: list,
                                expected: object, actual: object,
                                _constant_to_value: Dict[str, object]):
    """Return a failure message about the use of constants: after setting
    constants according to _constant_to_value, func(args) returned
    actual instead of expected,

    """

    return FAILURE_MESSAGE_CONSTANTS.format(
        _make_constants_and_values_msg(_constant_to_value),
        _make_call_string(func, args),
        expected, actual)


def _make_compare_constants_msg(func: callable, args: list,
                                expected: object,
                                _constant_to_value: Dict[str, object],
                                error: Exception) -> str:
    """Return a comparison error messagea about the use of constants:
    after setting constants according to _constant_to_value, comparing
    func(args) and expected raised an error."""

    return COMPARE_MESSAGE_CONSTANTS.format(
        _make_constants_and_values_msg(_constant_to_value),
        _make_call_string(func, args),
        expected, error)


def _make_constants_and_values_msg(_constant_to_value: Dict[str, object]) -> str:
    """Return a string const1 = val1\nconst2 = value2 ... from
    _constant_to_value.  """

    return '\n'.join(['{} = {}'.format(key, value)
                      for (key, value) in _constant_to_value.items()])

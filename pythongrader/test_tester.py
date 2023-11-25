"""Base class for testing the student test modules."""

import importlib
import sys
import unittest
import timeout_decorator

from .messages import (TESTER_FAILURE_FALSE_NEGATIVE_MESSAGE,
                       TESTER_FAILURE_FALSE_POSITIVE_MESSAGE)


class TestTesterBase(unittest.TestCase):
    """Testers of student tester modules."""

    def reloadFixture(self):
        self._fixture = sys.modules[self._get_module_name()]
        importlib.reload(self._fixture)

    def reloadTesterModule(self):
        self._tester_module = sys.modules[self._get_test_module_name()]
        importlib.reload(self._tester_module)

    def injectFunction(self, func):
        func_import_name = self._get_func_import_name()
        if hasattr(self._tester_module, func_import_name):
            setattr(self._tester_module, func_import_name, func)
        else:
            self.fail(
                f'no attribute {func_import_name} in {self._tester_module}')

    def _get_module_name(self):
        raise Exception("Override me.")

    def _get_test_module_name(self):
        raise Exception("Override me.")

    def _get_func_import_name(self):
        raise Exception("Override me.")

    def _check(self, correct: callable, bugs: dict[str, callable],
               description: str):

        self.reloadFixture()
        self.reloadTesterModule()

        # testing correct implementation should pass
        self.injectFunction(correct)
        self._run_tester_to_succeed()

        # testing buggy implementation should fail
        self.reloadTesterModule()
        self.injectFunction(bugs[description])
        self._run_tester_to_fail(description)

    def _run_tester_to_succeed(self):
        """Run the tester."""

        suite = unittest.TestLoader().loadTestsFromModule(self._tester_module)
        result = unittest.TextTestRunner().run(suite)

        msg = _make_test_failure_false_pos_msg()

        if not result.wasSuccessful():
            self.fail(msg)

    def _run_tester_to_fail(self, description: str):
        """Run the tester. If the result is successful, fail with
        description.

        """

        suite = unittest.TestLoader().loadTestsFromModule(self._tester_module)
        result = unittest.TextTestRunner().run(suite)

        msg = _make_test_failure_false_neg_msg(description)
        if result.wasSuccessful():
            self.fail(msg)


def auto_make_tests(testtester: unittest.TestCase, correct: callable,
                    bugs: dict[str, callable], timeout, start_count=1):
    """Create tests and add them to testtester. Each test runs _check() on
    one function from bugs.

    bugs maps descriptions to (broken) functions.

    """

    i = start_count
    for (description, func) in bugs.items():
        test_name = f'test_{i}_{func.__name__}'

        @timeout_decorator.timeout(timeout, use_signals=False)
        def new_test(self, correct=correct, description=description):
            checker = getattr(testtester, '_check')
            checker(self, correct, bugs, description)

        setattr(testtester, test_name, new_test)
        i += 1


def _make_test_failure_false_neg_msg(description):
    """Return a message that test module failed to detect a bug described
    in description.

    """

    return TESTER_FAILURE_FALSE_NEGATIVE_MESSAGE.format(description)


def _make_test_failure_false_pos_msg():
    """Return a message that test module failed on a correct implementation.

    """

    return TESTER_FAILURE_FALSE_POSITIVE_MESSAGE

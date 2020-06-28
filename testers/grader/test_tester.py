"""Base class for testing the student test modules.
"""

import importlib
import sys
from typing import Dict
import unittest
import timeout_decorator

from .config import TIMEOUT
from .messages import TEST_ERROR


class TestTesterBase(unittest.TestCase):
    """Testers of student tester modules."""

    def reloadFixture(self):
        self._fixture = sys.modules[self._get_module_name()]
        importlib.reload(self._fixture)

    def reloadTesterModule(self):
        self._tester_module = sys.modules[self._get_test_module_name()]
        importlib.reload(self._tester_module)

    def _get_module_name(self):
        raise Exception("Override me.")

    def _get_test_module_name(self):
        raise Exception("Override me.")

    def _check(self, fname: str, func: callable, description: str):
        self.reloadFixture()
        setattr(self._fixture, fname, func)
        self.reloadTesterModule()
        self._run_tester(description)

    @timeout_decorator.timeout(TIMEOUT)
    def _run_tester(self, description: str):
        """Run the tester. If the result is successful, fail with
        description.

        """

        suite = unittest.TestLoader().loadTestsFromModule(self._tester_module)
        result = unittest.TextTestRunner().run(suite)

        msg = _make_test_failure_msg(description)
        if result.wasSuccessful():
            self.fail(msg)


def auto_make_tests(testtester: unittest.TestCase, fname: str,
                    bugs: Dict[str, callable], start_count=1):
    """Create tests and add them to testtester. Each test runs _check() on
    one function from bugs.

    bugs maps descriptions to (broken) functions.

    """

    i = start_count
    for (description, func) in bugs.items():
        test_name = 'test_{}_{}'.format(i, func.__name__)

        def new_test(self, func=func, description=description):
            checker = getattr(testtester, '_check')
            checker(self, fname, func, description)
        setattr(testtester, test_name, new_test)
        i += 1


def _make_test_failure_msg(description):
    """Return a message that test module failed to detect a bug described
    in description.

    """

    return TEST_ERROR.format(description)

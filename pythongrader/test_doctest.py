"""Module to help test student doctests. Do not modify: use in your
own tester.

"""

import warnings
import unittest
import doctest
import timeout_decorator
from .config import TIMEOUT


EXISTS_FAILURE_MESSAGE = '''
{}'s docstring could not be found
'''

FAILURE_MESSAGE = '''
Some docstring examples from function {} failed doctest.
'''

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestDoctestBase(unittest.TestCase):
    """Base class for doctest testers."""

    def exists_test(self, fname, module):
        """Check that there is a function named fname with a docstring. If
        check succeeds, return (function, __doc__).

        """

        msg = EXISTS_FAILURE_MESSAGE.format(fname)

        # function exists
        if not hasattr(module, fname):
            self.fail(msg)

        func = getattr(module, fname)
        doc = func.__doc__

        # doc exists and is non-empty
        self.assertTrue(doc and doc.strip(), msg)

        return func, doc

    @timeout_decorator.timeout(TIMEOUT)
    def doctests_pass(self, fname, module):
        """Check that all doctests in f pass."""

        _, doc = self.exists_test(fname, module)

        doc_test = doctest.DocTestParser().get_doctest(
            doc, module.__dict__, f'doctests_{fname}',
            module.__name__, None)
        runner = doctest.DocTestRunner()
        runner.run(doc_test)
        failed, _ = runner.summarize()

        msg = FAILURE_MESSAGE.format(fname)
        self.assertFalse(failed, msg)  # no failed cases


def auto_make_test_from_functions(unittest_object, function_names, module):
    """Generate unittest test methods: one per function in function_names
    per method of TestDoctestBase.

    """

    for fname in function_names:
        test_name = f'test_doctests_pass_{fname}'
        test = TestDoctestBase.doctests_pass

        def new_test(self, fname=fname, test=test, module=module):
            return test(self, fname, module)
        setattr(unittest_object, test_name, new_test)

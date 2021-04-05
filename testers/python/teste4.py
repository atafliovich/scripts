"""Test E4."""

import operator
import re
import unittest
import timeout_decorator

from flake8.api import legacy as flake8
from pylint import epylint as lint

from grader.test_base import TestBase
from grader.utils import same_lists

try:
    import e4
except ImportError:
    pass

TIMEOUT = 10


class TestRecursion(TestBase):
    """Test function all_followers."""

    def _get_module_name(self):
        return 'e4'

    def testInterleave(self):

        func = e4.interleave

        self._test(func, [[], []], [])
        self._test(func, [[42], []], [])
        self._test(func, [[], [42]], [])
        self._test(func, [[1], [2]], [1, 2])
        self._test(func, [[1, 2, 3, 4], [5, 6, 42]],
                   [1, 5, 2, 6, 3, 42])
        self._test(func, [[1, 2, 3], [5, 6, 42, 7, 8]],
                   [1, 5, 2, 6, 3, 42])

    def testToPairs(self):

        func = e4.to_pairs
        self._test(func, [[], []], [])
        self._test(func, [[42], []], [])
        self._test(func, [[], [42]], [])
        self._test(func, [[1], [2]], [(1, 2)])
        self._test(func, [[1, 2, 3, 4], [5, 6, 42]],
                   [(1, 5), (2, 6), (3, 42)])
        self._test(func, [[1, 2, 3], [5, 6, 42, 7, 8]],
                   [(1, 5), (2, 6), (3, 42)])

    def testRepeat(self):

        func = e4.repeat
        def idf(x): return x
        def inc(x): return x + 1

        self._test(func, [idf, "foo", 0], ["foo"])
        self._test(func, [inc, 42, 1], [42, 43])
        self._test(func, [inc, 42, 3], [42, 43, 44, 45])

    def testNumNeg(self):

        func = e4.num_neg

        self._test(func, [[]], 0)
        self._test(func, [[1]], 0)
        self._test(func, [[1, 2, 3, 4]], 0)
        self._test(func, [[-1, -2, -3, -4]], 4)
        self._test(func, [[1, -2, 0, 4]], 1)

    def testGenSquares(self):

        func = e4.gen_squares
        self._test(func, [1, 1], [])
        self._test(func, [2, 3], [4])
        self._test(func, [5, 20], [36, 64, 100, 144, 196, 256, 324, 400])

    def testTriples(self):

        func = e4.triples
        self._test(func, [1], [], same_lists)
        self._test(func, [5], [(3, 4, 5)], same_lists)
        self._test(func, [15], [(3, 4, 5), (5, 12, 13),
                                (6, 8, 10), (9, 12, 15)], same_lists)
        self._test(func, [50],
                   [(3, 4, 5), (5, 12, 13), (6, 8, 10),
                    (7, 24, 25), (8, 15, 17), (9, 12, 15), (9, 40, 41),
                    (10, 24, 26), (12, 16, 20), (12, 35, 37),
                    (14, 48,  50), (15, 20, 25), (15, 36, 39),
                    (16, 30, 34), (18, 24, 30), (20, 21, 29),
                    (21, 28, 35), (24, 32, 40), (27, 36, 45), (30, 40, 50)],
                   same_lists)

    def testFlake8(self):
        '''Test that flake8 passes.'''

        style_guide = flake8.get_style_guide()
        report = style_guide.check_files(['e4.py'])
        self.assertEqual(report.get_statistics('E'),
                         [],
                         'Flake8 found violations')
        self.assertEqual(report.get_statistics('W'),
                         [],
                         'Flake8 found violations')

    def testPylint(self):

        # exit_code = lint.lint('recursion.py')
        # self.assertEqual(exit_code, 0, 'pylint reported some errors.')
        (pylint_stdout, pylint_stderr) = lint.py_run('e4.py', True)
        output = pylint_stdout.read().replace('\n', ' ')
        score = re.match(r'.*Your code has been rated at (\d+).*', output)
        self.assertTrue(score, 'pylint reported errors.')
        self.assertEqual(score.group(1), '10',
                         'pylint reported a non-perfect score.')

    @timeout_decorator.timeout(TIMEOUT)
    def _test(self, func, args, expected, comparator=operator.eq):
        (status, msg) = self._check(func, args, expected, comparator)
        if not status:
            self.fail(msg)

        (status, msg) = self._check_not_mutated(func, args)
        if not status:
            self.fail(msg)


if __name__ == '__main__':
    unittest.main(exit=False)

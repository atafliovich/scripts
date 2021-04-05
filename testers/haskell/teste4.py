"""Wrapper for pam.py to run. Until we write ram/sam."""

import os
import re
import subprocess
import unittest

FILE_NAME = 'E4.hs'
TEST_FILE_NAME = 'TestE4.hs'
OUTPUT_FILE = 'output.txt'
TIMEOUT = 2  # timeout for each function; make sure it is << global timeout

# function-name to max-marks-possible
FUNCTIONS = {"interleave": 6, "toPairs": 6, "repeat": 3,
             "numNeg": 3, "genSquares": 3, "triples": 4}


def run_all():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    results = FUNCTIONS.copy()

    for func in FUNCTIONS:
        run(func, results)

    return results


def run(func, results):
    if not os.path.isfile(FILE_NAME):
        return

    result = '{}:\n\t'.format(func)
    result_out, result_err = '', ''

    try:
        completed_process = subprocess.run(
            ['ghc', TEST_FILE_NAME, '-e', '{}Res'.format(func)],
            capture_output=True, timeout=TIMEOUT, text=True)
        result_out = completed_process.stdout.strip()
        result_err = completed_process.stderr
        result_err = re.sub(r'Cases(.*)\n', '', result_err).strip()
    except subprocess.TimeoutExpired:
        result += 'Timeout!\n'

    match = re.search(
        r'Counts {cases = (\d), tried = (\d), errors = (\d), failures = (\d)}',
        result_out)

    if match is None:
        print('Warning: could not record results for {}'.format(func))
    else:
        result += result_out + '\n\n'
        results[func] = int(match.group(3)) + int(match.group(4))

    result += result_err + '\n'

    with open(OUTPUT_FILE, 'a') as out:
        out.write(result)


class TestE4(unittest.TestCase):
    def _test_success(self, f_name):
        pass

    def _test_fail(self, f_name):
        self.fail(_msg(f_name))

    def test_hlint(self):
        self.assertTrue(os.path.isfile(FILE_NAME),
                        'No submission file {}.'.format(FILE_NAME))

        completed_process = subprocess.run(['hlint', FILE_NAME],
                                           capture_output=True,
                                           text=True)

        result_out = completed_process.stdout.strip()
        result_err = completed_process.stderr.strip()

        with open(OUTPUT_FILE, 'a') as out:
            out.write(result_out + '\n\n' + result_err)

        self.assertEqual(result_out, 'No hints',
                         'Errors reported by hlint. '
                         'See output.txt for details.')


def _msg(func_name):
    return "Errors in {}. See {} for details.".format(func_name,
                                                      OUTPUT_FILE)


def create_tests(unittest_object, test_success, test_fail, results):
    """Generate unittest test methods: one per function in function_names."""

    for f_name, num_fails in results.items():
        for i in range(num_fails):
            test_name = 'test_{}_{}'.format(f_name.replace('-', '_'), i)

            def new_test(self, f_name=f_name):
                return test_fail(self, f_name)

            setattr(unittest_object, test_name, new_test)
        for i in range(num_fails, FUNCTIONS[f_name]):
            test_name = 'test_{}_{}'.format(f_name.replace('-', '_'), i)

            def new_test(self, f_name=f_name):
                return test_success(self, f_name)

            setattr(unittest_object, test_name, new_test)


results = run_all()
create_tests(TestE4, TestE4._test_success, TestE4._test_fail, results)

if __name__ == '__main__':
    unittest.main(exit=False)

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 30


def timeout_operation(): return open("timedout", "w").close()


unittest_files = (
    'test_00_get_bridge.py',
    'test_01_get_average_bci.py',
    'test_02_get_total_length_on_hwy.py',
    'test_03_get_distance_between.py',
    'test_04_get_closest_bridge.py',
    'test_05_get_bridges_in_radius.py',
    'test_06_get_bridges_with_bci_below.py',
    'test_07_get_bridges_containing.py',
    'test_08_assign_inspectors.py',
    'test_09_inspect_bridges.py',
    'test_10_add_rehab.py',
    'test_11_format_data.py',
    'test_12_doctest.py',
    'test_13_docstrings.py',
    'test_14_constants.py',
    'test_pyta.py',
)
other_files = (
    'sanitize.py',
    'config.py',
    'constants.py',
)

where = '/home/anya/a08/assignments/a2'

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname = f'{where}/marking/directories.txt'

# where are the templates?
template_dir = "templates"

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = (
    ';'.join([f'cp {where}/unittests/{cp_file} .'
              for cp_file in unittest_files + other_files])
)

test_cmd = [
    'python3.11 sanitize.py && '
    'python3.11 /home/anya/at/pam/pam.py --timeout 10 result.json '
    + ' '.join(unittest_files)]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = f"rm -rf {' '.join(unittest_files + other_files)}"

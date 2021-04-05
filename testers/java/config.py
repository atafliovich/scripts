import subprocess

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 100


def timeout_operation(): return open("timedout", "w").close()


# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname = "/home/anya/c24/exercises/e4/marking/java/directories.txt"
#students_fname = "/home/anya/c24/exercises/e4/marking/java/short.txt"

# where are the templates?
template_dir = "templates"

preamble_cmd = (
    "cp -R /home/anya/c24/exercises/e4/solution/E4/src/polytests .; "
    "cp /home/anya/c24/exercises/e4/marking/java/test_e4.py .; "
    "rm -f */*.class compile.txt result*")

test_cmd = ['python3.7 test_e4.py']

postamble_cmd = 'rm -rf polytests test_e4.py'

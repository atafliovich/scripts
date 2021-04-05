# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 100000  # pylint takes a long time


def timeout_operation(): return open("timedout", "w").close()


students_fname = "/home/anya/c24/exercises/e4/marking/python/directories.txt"

template_dir = "templates"

preamble_cmd = "cp -R /home/anya/c24/exercises/e4/marking/python/teste4.py /home/anya/c24/exercises/e4/marking/python/grader ."

test_cmd = [
    "python3.8 /home/anya/at/pam/pam.py --timeout 1000 result_python.json teste4.py"]

postamble_cmd = ("rm -rf __pycache__ *.pyc teste4.py grader")

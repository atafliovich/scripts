
# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 30


def timeout_operation(): return open("timedout", "w").close()


# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname = "/home/anya/c24/exercises/e4/marking/haskell/directories.txt"

# where are the templates?
template_dir = "templates"

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = ("cp /home/anya/c24/exercises/e4/marking/haskell/TestE4.hs .; "
                "cp /home/anya/c24/exercises/e4/marking/haskell/teste4.py .")

test_cmd = [
    "python3.7 /home/anya/at/pam/pam.py --timeout 10 result_haskell.json teste4.py"]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = "rm -rf __pycache__ compiled TestE4.hs *.py *.hi *.o TestE4"

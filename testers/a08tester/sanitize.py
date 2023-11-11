"""Check for disallowed imports."""

import os
import sys

FILENAME = 'bridge_functions.py'
PYTA_LOCATION = '/home/anya/a08/assignments/a2/starter/pyta'
PYTA_CONFIG_FILE = 'a2_pyta.txt'
PYTA_OUT_FILENAME = 'errors.txt'

FILEPATH = os.path.join(os.getcwd(), FILENAME)
PYTA_OUT_FILEPATH = os.path.join(os.getcwd(), PYTA_OUT_FILENAME)
PYTA_CONFIG_PATH = os.path.join(PYTA_LOCATION, PYTA_CONFIG_FILE)

sys.path.insert(0, PYTA_LOCATION)  # noqa
import python_ta  # noqa


reporter = python_ta.check_errors(
    FILEPATH, PYTA_CONFIG_PATH, PYTA_OUT_FILEPATH, True, False)

for msg in reporter.messages[FILEPATH]:
    if msg.msg_id == 'E9999':
        print("Disallowed imports. Refusing to run testers.")
        sys.exit(1)

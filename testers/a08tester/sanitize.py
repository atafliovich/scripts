"""Check for disallowed imports."""

import os
import sys

from config import FILENAME, PYTA_LOCATION, PYTA_CONFIG_FILE

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
        os.rename(FILEPATH,
                  os.path.join(os.getcwd(), f'disallowed.{FILENAME}'))
        print("Disallowed imports. Refusing to run testers.")
        sys.exit(1)

os.remove(PYTA_OUT_FILEPATH)

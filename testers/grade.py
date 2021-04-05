""" Work with MarkUs.
"""

import sys
import canvasapi
import markusapi

import gradeutils
import markusutils

sys.path.append('/home/anya/scripts')  # NOQA: E402
from admin import students  # noqa
from admin import gradebook as gb  # noqa
from canvas import utils as canvasutils  # noqa

MARKUS_API_KEY = ''
QUERCUS_API_KEY = ''
QUERCUS_COURSE_ID = ''

COURSE = 'cscc24w21'
CONFIG = 'config.py'

ASSIGNMENT_ID = 12
ASSIGNMENT_NAME = 'lab8'

MARKING_DIR = '/home/anya/c24/labs/08/marking'
LOCAL_DIR = 'submissions'

# paths relative to student repo directory (utorid on MarkUs)
MARKUS_FILES = ['Lab8.hs']
LOCAL_FILES = ['Lab8.hs']

RESULT_FILES = {  # without exptension
    'result'
}

RESULT_FILES_TO_WEIGHTS = {'result': 'weights.gf'}

UPLOAD_FILES = {  # with exptension
    'output.txt',
    'result.txt'
}

GF_MARKS = {"apply": 4, "element": 5, "replace": 5, "sumLeafs": 4,
            "numNodes": 3, "numLevels": 3, "flip": 3, "hlint": 1}
CRITERIA = {"apply": 2, "element": 2, "replace": 2, "sumLeafs": 2,
            "numNodes": 2, "numLevels": 2, "flip": 3, "hlint": 3}

########################################################################
# MarkUs
URL = 'https://markus.utsc.utoronto.ca/{}'.format(COURSE)
API = markusapi.Markus(MARKUS_API_KEY, URL)

# Quercus
Q_API_URL = 'https://q.utoronto.ca'
CANVAS = canvasapi.Canvas(Q_API_URL, QUERCUS_API_KEY)
COURSE = CANVAS.get_course(QUERCUS_COURSE_ID)

# submissions info
GROUPS = API.get_groups(ASSIGNMENT_ID)
UTORID_TO_GROUP = markusutils.get_utorid_to_group(API, ASSIGNMENT_ID)

# map function-name-in-gf-file to
# (function-name-markus-criteria, gf-out-of, markus-out-of)
CRITERIA_MAPS = [
    {name: (name, GF_MARKS[name], CRITERIA[name])
     for (name, outof) in criteria.items()}
    for criteria in (GF_MARKS,)]

########################################################################


def get_submissions():
    markusutils.get_submissions(API, ASSIGNMENT_ID, MARKUS_FILES, LOCAL_DIR,
                                LOCAL_FILES)


def setup_tester():
    gradeutils.setup_tester(COURSE, MARKING_DIR, LOCAL_DIR)


def test_all(run, aggregate, template, gen):
    gradeutils.test_all(MARKING_DIR, LOCAL_DIR, CONFIG, ASSIGNMENT_NAME,
                        RESULT_FILES, RESULT_FILES_TO_WEIGHTS,
                        run, aggregate, template, gen)


def upload_files():
    for UPLOAD_FILE in UPLOAD_FILES:
        markusutils.upload_result_files(
            API, ASSIGNMENT_ID, LOCAL_DIR, UPLOAD_FILE)


def upload_grades():
    for (RESULT_FILE, CRITERIA_MAP) in zip(RESULT_FILES, CRITERIA_MAPS):
        with open('{}.gf'.format(RESULT_FILE)) as GF_FILE:
            markusutils.upload_grades(
                API, ASSIGNMENT_ID, GF_FILE, CRITERIA_MAP, False)


def test_one(utorid, redownload=False, run=True, aggregate=True,
             template=True, gen=True, upload_grades=True, upload_files=True):
    """Test one submission."""

    if redownload:
        print('Redownloading {}...'.format(utorid))
        markusutils.get_submission(API, ASSIGNMENT_ID, MARKUS_FILES, LOCAL_DIR,
                                   LOCAL_FILES, utorid)
        gradeutils.setup_tester(COURSE, MARKING_DIR, LOCAL_DIR)
        print('Done redownloading.')

    gradeutils.test_one(utorid, MARKING_DIR, LOCAL_DIR, CONFIG,
                        ASSIGNMENT_NAME, RESULT_FILES,
                        RESULT_FILES_TO_WEIGHTS)

    if upload_grades:
        for (RESULT_FILE, CRITERIA_MAP) in zip(RESULT_FILES, CRITERIA_MAPS):
            print('Uploading grades {} for {}...'.format(RESULT_FILE, utorid))
            with open('{}.gf'.format(RESULT_FILE)) as GF_FILE:
                markusutils.upload_grade(
                    API, ASSIGNMENT_ID, CRITERIA_MAP,
                    utorid, None, GF_FILE, None, False)
            print('Done.')

    if upload_files:
        print('Uploading files for {}...'.format(utorid))
        for UPLOAD_FILE in UPLOAD_FILES:
            markusutils.upload_result_file(API,
                                           ASSIGNMENT_ID,
                                           LOCAL_DIR,
                                           UPLOAD_FILE,
                                           utorid)


def clean_repos():
    for utorid, group in UTORID_TO_GROUP.items():
        for UPLOAD_FILE in UPLOAD_FILES:
            API.remove_file_from_repo(ASSIGNMENT_ID, group['id'], UPLOAD_FILE)


# clean_repos()

# with open('criteria_auto.yml', 'w') as outfile:
#     gradeutils.write_criteria_file(CRITERIA, outfile)

# get_submissions()

# setup_tester()

# test_all(True, True, True, False)
# test_all(False, False, False, True)

# upload_files()

# upload_grades()

# test_one('franc272', redownload=False, run=True, aggregate=True,
#          template=True, gen=True, upload_grades=True, upload_files=True)

# test_one('saqeebna', redownload=True, run=False, aggregate=False,
#          template=False, gen=False, upload_grades=False, upload_files=False)

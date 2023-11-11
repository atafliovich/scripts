"""Autograde assignment."""

import os
import string
import sys
import canvasapi
import markusapi

from publicconfig import (
    MARKUS_URL, QUERCUS_URL, MARKUS_COURSE_ID, QUERCUS_COURSE_ID)
from privateconfig import (
    SCRIPTS_DIR, COURSE_DIR, MARKUS_API_KEY, QUERCUS_API_KEY)

sys.path.append(SCRIPTS_DIR)  # noqa
from admin import students  # noqa
from admin import gradebook as gb  # noqa
from canvas import utils as canvasutils  # noqa
from uamutils import gradeutils  # noqa
from markusutils import markusutils  # noqa


CONFIG = 'a2config.py'

ASSIGNMENT_ID = 99
ASSIGNMENT_NAME = 'a2'

MARKING_DIR = os.path.join(COURSE_DIR, 'assignments', 'a2', 'marking')
LOCAL_DIR = 'submissions'

# paths relative to student repo directory (utorid on MarkUs)
MARKUS_FILES = ['bridge_functions.py']
LOCAL_FILES = ['bridge_functions.py']

TEMPLATE_FILE = 'individual_short.tpl'
RESULT_FILES = {  # without extension
    'result'
}

RESULT_FILES_TO_WEIGHTS = {'result': 'weights.gf'}

UPLOAD_FILES = {  # with extension
    'result.txt',
    'pyta_output.txt'
}

GF_MARKS = {  # TODO
    'get_bridge': 1,
    'get_average_bci': 1,
    'get_total_length_on_hwy': 1,
    'get_distance_between': 1,
    'get_closest_bridge': 1,
    'get_bridges_in_radius': 1,
    'get_bridges_with_bci_below': 1,
    'get_bridges_containing': 1,
    'assign_inspectors': 1,
    'inspect_bridges': 1,
    'add_rehab': 1,
    'format_data': 1,
    'doctests': 1,
    'docstrings': 1,
    'constants': 1,
    'pyta': 20
}

CRITERIA = {
    'get_bridge': 2,
    'get_average_bci': 2,
    'get_total_length_on_hwy': 2,
    'get_distance_between':  2,
    'get_closest_bridge':  4,
    'get_bridges_in_radius':  4,
    'get_bridges_with_bci_below':  4,
    'get_bridges_containing':  2,
    'assign_inspectors':  6,
    'inspect_bridges':  3,
    'add_rehab':  3,
    'format_data':  6,
    'doctests': 3,
    'docstrings': 3,
    'constants': 4,
    'pyta': 10
}


########################################################################
# MarkUs
API = markusapi.Markus(MARKUS_API_KEY, MARKUS_URL)

# Quercus
CANVAS = canvasapi.Canvas(QUERCUS_URL, QUERCUS_API_KEY)
COURSE = CANVAS.get_course(QUERCUS_COURSE_ID)

# submissions info
GROUPS = API.get_groups(MARKUS_COURSE_ID, ASSIGNMENT_ID)
UTORID_TO_GROUP = markusutils.get_utorid_to_group(
    API, MARKUS_COURSE_ID, ASSIGNMENT_ID)
UTORIDS = UTORID_TO_GROUP.keys()

TA_UTORIDS = []

GF_DATA = (GF_MARKS,)
GF_TO_CRITERIA_FUNC_NAMES = dict(zip(GF_MARKS.keys(), GF_MARKS.keys()))

#############################################################################

# map function-name-in-gf-file to
# (function-name-markus-criteria, gf-out-of, markus-out-of)
CRITERIA_MAPS = [
    {name: (GF_TO_CRITERIA_FUNC_NAMES[name],
            GF_MARKS[name],
            CRITERIA[GF_TO_CRITERIA_FUNC_NAMES[name]])
     for (name, outof) in criteria.items()}
    for criteria in GF_DATA]

########################################################################


def get_submissions(group='students'):
    """Get student/TA submissions from MarkUs."""

    markusutils.get_submissions(
        API, MARKUS_COURSE_ID, ASSIGNMENT_ID,
        MARKUS_FILES, LOCAL_DIR, LOCAL_FILES,
        UTORIDS if group == 'students' else TA_UTORIDS)


def setup_tester(target_group='student'):
    """Setup autotester files."""

    gradeutils.setup_tester(COURSE, MARKING_DIR, LOCAL_DIR, target_group)


def test_all(run: bool, aggregate: bool, template: bool, gen: bool):
    """Test all submissions."""

    gradeutils.test_all(
        MARKING_DIR, LOCAL_DIR, CONFIG,
        ASSIGNMENT_NAME, RESULT_FILES, RESULT_FILES_TO_WEIGHTS,
        run, aggregate, template, gen, TEMPLATE_FILE)


def upload_all_files(group='students'):
    """Upload result files to MarkUs."""

    for upload_file in UPLOAD_FILES:
        markusutils.upload_result_files(
            API, MARKUS_COURSE_ID, ASSIGNMENT_ID, LOCAL_DIR, upload_file,
            TA_UTORIDS if group == 'tas' else UTORIDS)


def upload_all_grades(group='students'):
    """Upload grades to MarkUs."""

    for (result_file, criteria_map) in zip(RESULT_FILES, CRITERIA_MAPS):
        with open(f'{result_file}.gf', encoding='UTF-8') as gf_file:
            markusutils.upload_grades(
                API, MARKUS_COURSE_ID, ASSIGNMENT_ID,
                gf_file, criteria_map, False)


def test_one(utorid, redownload=False,
             run=True, aggregate=True, template=True, gen=True,
             upload_grades=True, upload_files=True,
             template_file=TEMPLATE_FILE):
    """Test one submission."""

    if redownload:
        print(f'Redownloading {utorid}...')
        markusutils.get_submission(
            API, MARKUS_COURSE_ID, ASSIGNMENT_ID,
            MARKUS_FILES, LOCAL_DIR, LOCAL_FILES, utorid)
        gradeutils.setup_tester(COURSE, MARKING_DIR, LOCAL_DIR)
        print('Done redownloading.')

    gradeutils.test_one(
        utorid, MARKING_DIR, LOCAL_DIR, CONFIG,
        ASSIGNMENT_NAME, RESULT_FILES, RESULT_FILES_TO_WEIGHTS,
        run, aggregate, template, gen, template_file)

    if upload_grades:
        for (result_file, criteria_map) in zip(RESULT_FILES, CRITERIA_MAPS):
            print(f'Uploading grades {result_file} for {utorid}...')
            with open(f'{result_file}.gf',  encoding='utf8') as gf_file:
                markusutils.upload_grade(
                    API, MARKUS_COURSE_ID, ASSIGNMENT_ID, criteria_map,
                    utorid, None, gf_file, None, False)
            print('Done.')

    if upload_files:
        print(f'Cleaning up output files for {utorid}...')
        clean_output_files(utorid)
        print(f'Uploading files for {utorid}...')
        for upload_file in UPLOAD_FILES:
            markusutils.upload_result_file(
                API, MARKUS_COURSE_ID, ASSIGNMENT_ID, LOCAL_DIR,
                upload_file, utorid)


def clean_repos():
    """Remove result files from all repos on MarkUs."""

    for group in UTORID_TO_GROUP.values():
        for upload_file in UPLOAD_FILES:
            API.remove_file_from_repo(
                MARKUS_COURSE_ID, ASSIGNMENT_ID, group['id'], upload_file)


def clean_output_files(utorid=None):
    """Remove special charcaters from result files, because MarkUs can
    reject them.

    """

    printable = set(string.printable)
    utorids = [utorid] if utorid else UTORIDS
    for utid in utorids:
        for output_file in UPLOAD_FILES:
            try:
                with open(f'submissions/{utid}/{output_file}',
                          encoding='utf8') as orig_f:
                    content = ''.join(
                        [char for char in orig_f.read() if char in printable])
                    with open(f'submissions/{utid}/{output_file}',
                              'w', encoding='utf8') as new_f:
                        new_f.write(str(content))
            except FileNotFoundError:
                print(f'Warning: no result file for {utid}')
                continue

# clean_repos()


# get_submissions('tas')
# get_submissions()

# setup_tester()
# setup_tester('ta')

# with open('criteria.yml', 'w', encoding='utf-8') as outfile:
#     gradeutils.write_criteria_file(CRITERIA, outfile)

# test_all(run, aggregate, template, gen)
# test_all(True, False, False, False)
# test_all(False, True, True, True)

# clean_output_files()
# upload_files('tas')
# upload_grades('tas')
# upload_all_files()
# upload_all_grades()


# test_one('tafliovi', redownload=False, run=True, aggregate=False,
#         template=False, gen=False, upload_grades=False, upload_files=False)

"""Download/uplpoad to/from Quercus.
"""

import sys
from canvasapi import Canvas
sys.path.append('/home/anya/scripts')
# pylint: disable=wrong-import-position
import admin.gradebook as gb

API_URL = 'https://q.utoronto.ca'

# Go to https://q.utoronto.ca/profile/settings to generate an Access
# Token. Copy it immediately and paste here.
API_KEY = ''


# This is the course ID. The easiest way to get it is to look at the
# URL.  For example, my CSCC01 on Quercus is
# https://q.utoronto.ca/courses/158528 and so the ID of this course is
# "158528".
COURSE_ID = ''

# Map of students.Student attributes to canvasapi.Usert attributes.
KEY_MAP = {
    'student_number': 'integration_id',
    'utorid': 'login_id'
}

def download_asst_grades(course, asst_name, key='student_number'):
    """Return a Dict[key, grade: float]

    course is a canvasapi.Course.
    asst_name is the name of the assignment to download grades from.
    key is the key in the return dict: 'utorid' or 'student_number'.
    """

    assignment = _get_assignment(course, asst_name)
    submissions = assignment.get_submissions()

    attr2grade = {getattr(KEY_MAP[key], course.get_user(submission.user_id)):
                  float(submission.score) if submission.score else 0.0
                  for submission in submissions}

    return attr2grade


def upload_new_asst_grades(course, attribute_to_grade,
                           assignment_name='Assignment', out_of=None,
                           assignment_group_id=None):
    """Upload new assignment grades to quercus.

    course is a canvasapi.Course.
    assignment_name is the name of the new canvasapi.Assignment.
    attribute_to_grade is a Dict[attribute, grade:float] where attribute
      is utorid or student_number.
    out_of is maximum number of marks on this assignment.

    """

    specs = {
        'name': assignment_name,
        'assignment_group_id': assignment_group_id,
        'points_possible': out_of,
        'hide_results': 'always',
        'published': True  # can't bulk_apdate if not published!
    }

    assignment = course.create_assignment(specs)

    grade_data = {_get_user_id(course, attr): {'posted_grade': grade}
                  for (attr, grade) in attribute_to_grade.items()}

    assignment.submissions_bulk_update(grade_data=grade_data)


def upload_grades(course, gffile, attr='student_number'):
    """Upload all grades in gffile to Quercus (as new assignments).

    course is a canvasapi.Course.
    gffile is a .gf file open for reading.
    """

    grbook = gb.GradeBook.load_gf_file(gffile)
    upload_gradebook(course, grbook, attr)


def upload_gradebook(course, gradebook, attr='student_number'):
    """Upload all grades in gradebook to Quercus (as new assignments).

    course is a canvasapi.Course.
    gradebook is a gradebook.GradeBook.
    attr is Student attribute to use as keys (e.g., 'utorid' or 'student_number').
    """

    assert gradebook.outofs is not None

    for asst_name, outof in gradebook.outofs.items():
        attr_to_grade = gradebook.get_grades_dict(asst_name, attr)
        upload_new_asst_grades(course, attr_to_grade, asst_name, outof)


def _get_user_id(course, attribute):
    result = list(filter(lambda user: attribute in (user.login_id, user.integration_id),
                         course.get_users()))
    assert len(result) == 1
    return result[0].id


def _get_assignment(course, name):
    result = list(course.get_assignments(search_term=name))
    result = list(filter(lambda a: a.name == name, result))
    assert len(result) == 1
    return result[0]


if __name__ == '__main__':
    CANVAS = Canvas(API_URL, API_KEY)
    COURSE = CANVAS.get_course(COURSE_ID)

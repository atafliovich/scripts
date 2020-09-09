"""Download/uplpoad to/from Quercus.
"""

from datetime import date
import os
import random
import sys

from canvasapi import Canvas

sys.path.append('/home/anya/scripts')  # NOQA: E402
import admin.gradebook as gb
import admin.students as sts

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
    'utorid': 'sis_user_id'
}

# Default format in which to write a classlist file. Here id1 is Quercus id.
CLASSLIST_FORMAT = ('last', 'first', 'utorid',
                    'student_number', 'id1', 'email')


def download_students(course, key='student_number'):
    """Return admin.students.Students.

    course is a canvasapi.Course.
    key is the key in the return Students (e.g., 'utorid' or 'student_number').
    """

    return _download_role(course, 'student', key)


def download_tas(course, key='student_number'):
    """Return admin.students.Students.

    course is a canvasapi.Course.
    key is the key in the return Students (e.g., 'utorid' or 'student_number').
    """

    return _download_role(course, 'ta', key)


def _download_role(course, role, key='student_number'):
    users = _get_role(course, role)
    students = (_canvas_user_to_student(user) for user in users)
    return sts.Students(students, key)


def _canvas_user_to_student(user):
    return sts.Student(
        utorid=getattr(user, KEY_MAP['utorid']),
        student_number=getattr(user, KEY_MAP['student_number']),
        last=user.name.split()[-1],
        first=' '.join(user.name.split()[:-1]),
        email=getattr(user, 'email', 'fake@utoronto.ca').replace(
            'noemail', 'mail'),  # TODO: HACK. WTF is going on with emails on Quercus?
        id1=str(user.id))  # this is Quercus ID


def download_asst_grades(course, asst_name, key='student_number'):
    """Return a Dict[key, grade: float]

    course is a canvasapi.Course.
    asst_name is the name of the assignment to download grades from.
    key is the key in the return dict: 'utorid' or 'student_number'.
    """

    assignment = _get_assignment(course, asst_name)
    submissions = assignment.get_submissions()

    attr2grade = {getattr(course.get_user(submission.user_id), KEY_MAP[key]):
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


def write_classlist(course, path_prefix, classlist_format=CLASSLIST_FORMAT):
    """Download current student data from Quercus and write today's
    classlist to file path_prefix/classlist_month_day.csv.

    course is a canvasapi.Course

    """

    _write_roster_file(course, 'student', path_prefix, classlist_format)


def write_ta_list(course, path_prefix, list_format=CLASSLIST_FORMAT):
    """Download current TA data from Quercus and write today's
    TA list to file path_prefix/classlist_month_day.csv.

    course is a canvasapi.Course

    """

    _write_roster_file(course, 'ta', path_prefix, list_format)


def _write_roster_file(course, role, path_prefix, list_format=CLASSLIST_FORMAT):

    users = _download_role(course, role)
    with open(os.path.join(path_prefix,
                           '{}list_{}_{}.csv'.format(
                               'TA' if role.lower() == 'ta' else 'class',
                               date.today().month,
                               date.today().day)),
              'w') as outfile:
        users.write_classlist(outfile, list_format)


def write_breakout_rooms(course, num_students_per_room, path_prefix='.'):
    """Download current student data from Quercus and write lists for
    uploading to zoom for creatring breakout rooms to files
    path_prefix/month_day_section.csv (e.g., 9_8_LEC01.csv)

    course is a canvasapi.Course
    num_students_per_room is the number of students to assign to each room

    """

    sections = course.get_sections(include=['students'])

    for section in sections:
        filename = os.path.join(path_prefix,
                                '{}_{}_{}.csv'.format(date.today().month,
                                                      date.today().day,
                                                      section.name.split('-')[2]))
        num_rooms = len(section.students) // num_students_per_room
        emails = [course.get_user(student['id'], include=['email']).email
                  for student in section.students]
        _write_breakout_rooms_one_section(emails, num_rooms, filename)


def _write_breakout_rooms_one_section(emails, num_rooms, filename):
    """Create a file named filename for uploading to zoom to pre-assign
    breakout rooms.

    """

    random.shuffle(emails)
    with open(filename, 'w') as outfile:
        outfile.write('Pre-assign Room Name,Email Address\n')
        for i, email in enumerate(emails):
            outfile.write('room{},{}\n'.format(i % num_rooms, email))


def _get_user_by_utorid(course, utorid):
    return course.get_user(utorid, 'sis_login_id')


def _get_userid_by_utorid(course, utorid):
    return course.get_user(utorid, 'sis_login_id').id


def _get_user_id(course, attribute):
    result = list(filter(lambda user: attribute in (user.login_id, user.integration_id),
                         course.get_users()))
    assert len(result) == 1
    return result[0].id


def _get_tas(course):
    return _get_role(course, 'ta')


def _get_students(course):
    return _get_role(course, 'student')


def _get_role(course, role):
    return list(course.get_users(enrollment_type=[role], include=['email']))


def _get_assignment(course, name):
    result = list(course.get_assignments(search_term=name))
    result = list(filter(lambda a: a.name == name, result))
    assert len(result) == 1
    return result[0]


if __name__ == '__main__':
    CANVAS = Canvas(API_URL, API_KEY)
    COURSE = CANVAS.get_course(COURSE_ID)

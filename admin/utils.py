"""A new set of utilities to work with MarkUs, Quercus, Intranet, CDF
grades files, CATME files, and what not.
Work in progress.

"""

from .defaults import DEFAULT_STUDENT_STR, default_student_sort, DEFAULT_CATME_STR
from .gradebook import GradeBook


# TODO def make_csv_grades_file

def write_catme_from_students(students, outfile,
                              attrs=DEFAULT_CATME_STR, header=True,
                              key=default_student_sort):
    '''Write out a CATME student file to outfile.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    attrs is an iterable of attributes of Student to include.
    key is the key for sorting Students.
    header is True/False: whether to write the header
    '''

    students.write_catme(outfile, attrs, header, key)


def write_classlist_from_students(students, outfile,
                                  attrs=DEFAULT_STUDENT_STR, header=False,
                                  key=default_student_sort):
    '''Write out a CSV classlist to outfile.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    attrs is an iterable of attributes of Student to include.
    key is the key for sorting Students.
    header is True/False: whether to write the header
    '''

    students.write_classlist(outfile, attrs, header, key)


def write_gf_from_students(students, outfile, outofs=None, utorid=True,
                           key=default_student_sort):
    '''Write out an empty gf file.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    outofs is a Dict[asst:str, outof:int] for the header.
    key is the key for sorting Students.
    utorid is True/False: whether to include utorids.
    '''

    students.write_gf(outfile, outofs, utorid, key)


def write_gf_from_dict(outfile, stnum_to_student_grades, outofs,
                       utorid=True, key=default_student_sort):
    '''Write a gf file to outfile.

    stnum_to_student_grades is Dict[stnum, Tuple(Student, Grades)]
    outofs is a List[(asst, grade)] since it must be ordered for gf.

    '''

    gradebook = GradeBook(stnum_to_student_grades, 'student_number', outofs)
    gradebook.write_gf(outfile, utorid, key)


def make_csv_submit_file(outfile, dict_key_to_student_grades, asst,
                         dict_key, exam_no_shows):
    '''Write a CSV submit file for eMarks to outfile.

    dict_key_to_student_grades maps dict_key to Tuple(Student, Grades).
    asst is the name of the "final mark" assignment.
    dict_key is some key (normally student_number or utorid) into the dict.
    exam_no_shows is a list of dict_keys of exam no shows.

    '''

    gradebook = GradeBook(dict_key_to_student_grades, dict_key)
    gradebook.write_csv_submit_file(outfile, asst, exam_no_shows, dict_key)


def load_quercus_grades_file(infile, dict_key='student_number'):
    '''Read Quercus CSV Gradebook.
    Return (Dict[dict_key, Tuple(Student, Grades)], outofs).
    The default dictionary key is student_number. Another common use case would be 'utorid'.
    See also StudentGrades' staticmethod.
    '''

    student_grades = GradeBook.load_quercus_grades_file(infile, dict_key)
    return student_grades.studentgrades, student_grades.outofs


def load_gf_file(infile, dict_key='student_number'):
    '''Read gf grades file.
    Return (Dict[dict_key, Tuple(Student, Grades)], outofs).
    The default dictionary key is student_number. Another common use case would be 'utorid'.
    See also StudentGrades' staticmethod.
    '''

    student_grades = GradeBook.load_gf_file(infile, dict_key)
    return (student_grades.studentgrades, student_grades.outofs)


def make_team_to_students(students):
    '''Return a dict mapping team name to Student list.
    students is a Students object.

    '''

    team_to_students = {}
    for student in students:
        members = team_to_students.get(student.team, [])
        members.append(student)
        team_to_students[student.team] = members
    return team_to_students


def make_team_to_emails(students):
    '''Return a dict mapping team name to list of emails of team members.
    students is a Students object.

    '''

    team_to_emails = {}
    for student in students:
        emails = team_to_emails.get(student.team, [])
        emails.append(student.email)
        team_to_emails[student.team] = emails
    return team_to_emails


def make_yaml_grading_sheet(students, team_to_ta_email):
    '''Return a List[dict] that can be dumped to YAML for Thierry's
    grading rubric.

    '''

    team_to_emails = make_team_to_emails(students)

    to_yaml = []
    for team, emails in team_to_emails.items():
        sheet = team
        write = [team_to_ta_email[team]]
        audit = [ta_email for ta_email in set(team_to_ta_email.values())
                 if ta_email not in write]
        read = emails
        to_yaml.append({'sheet': sheet, 'write': write,
                        'audit': audit, 'read': read})
    return to_yaml

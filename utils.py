"""A new set of utilities to work with MarkUs, Quercus, Intranet, CDF
grades files, CATME files, and what not.
Work in progress. This is the DB version.

"""

from pprint import pprint
from pymongo import MongoClient

from defaults import DEFAULT_STUDENT_STR, default_student_sort
from gradebook import GradeBook


'''
# mongo "mongodb+srv://cluster0-8mamn.gcp.mongodb.net/test"  --username atafliovich
CLIENT = MongoClient()
DB = CLIENT.studentgrades
'''


# TODO def make_csv_grades_file


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

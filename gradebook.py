'''My gradebook.'''

import csv
import json
import math
import re

from defaults import default_student_sort, DEFAULT_FORMULA_OUTOF
from shared import _make_gf_header, _make_gf_student_line
from students import Student, Students


class GradeBook:
    '''My own gradebook.'''

    def __init__(self, studentgrades=None, dict_key='student_number',
                 outofs=None, comments=None):
        '''Init a Gradesfile given:

        outofs: Dict[str, float] maps assigment name to max possible grade.
        studentgrades: Dict[dict_key, Tuple(Student, Grades)].
        dict_key: a Student attribute; key into studentgrades and comments.
           Most likely student_number or utorid.
        comments: Dict[dict_key, str].

        '''

        self.outofs = dict(outofs) if outofs else {}
        self.studentgrades = dict(studentgrades) if studentgrades else {}
        self.dict_key = dict_key
        # TODO validate_studentgrades(self.student_grades, self.dict_key, self.outofs)
        self.comments = dict(comments) if comments else {}
        # TODO validate_comments(self.comments, self.dict_key)

    def __iter__(self):
        return iter(self.studentgrades)

    def __str__(self):
        result = str(self.outofs) + '\n\n'

        student_list = _sorted_student_grades(self.studentgrades)
        for student, grades in student_list:
            key = getattr(student, self.dict_key)
            result += '{}: {},{},{}\n'.format(
                key,
                student,
                grades,
                self.comments.get(key, ''))
        return result

    def get_students(self):
        '''Return a Students object with this StudentGrades' students.'''

        return Students(record[0] for record in self.studentgrades.values())

    def get_student_grades_by_utorid(self, utorid):
        '''Return Grades of a Student with utorid. Raise NoSuch? if no such Student.'''

        return self.get_student_grades_by_attribute('utorid', utorid)

    def get_student_grades_by_student_number(self, student_number):
        '''Return Grades of a Student with student_number. Raise NoSuch? if no such Student.'''

        return self.get_student_grades_by_attribute('student_number', student_number)

    def get_student_grades_by_attribute(self, attribute, attr_value):
        '''Return Grades of a Student with value of attribute equal to
        attr_value.  Raise NoSuch? if no such Student. Raise
        AttributeError if attribute is not present in at least one
        Student.

        '''

        for student, grades in self.studentgrades.values():
            if getattr(student, attribute) == attr_value:
                return grades
        raise Exception('No student with {} value {}.'.format(
            attribute, attr_value))

    def get_dict(self, key):
        '''Return a Dict[key, Tuple(Student, Grades).
        Useful when self.key = 'student_number' and we want the dict by 'utorid',
        for example.'''

        if key == self.dict_key:
            return self.studentgrades

        new_key_to_student_grades = {}
        for student, grades in self.studentgrades.values():
            try:
                key = getattr(student, key)
                new_key_to_student_grades[key] = (student, grades)
            except AttributeError:
                print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                    key, student))
        return new_key_to_student_grades

    @staticmethod
    def load_quercus_grades_file(infile, dict_key='student_number'):
        '''Read Quercus CSV Gradebook.
        The default dictionary key is student_number. Another common
        use case would be 'utorid'.

        '''

        reader = csv.DictReader(infile)
        dict_key_to_student_grades = {}

        for row in reader:
            first = row['Student'].strip()
            if first == 'Points Possible':
                outofs = _make_out_of_from_quercus_row(row)
                continue

            student = Student.make_student_from_quercus_row(row)
            if not student:
                continue

            grades = Grades.make_grades_from_quercus_row(row)

            try:
                key = getattr(student, dict_key)
                dict_key_to_student_grades[key] = (student, grades)
            except AttributeError:
                print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                    dict_key, student))

        return GradeBook(dict_key_to_student_grades, dict_key, outofs)

    @staticmethod
    def load_gf_file(infile, dict_key='student_number'):
        '''Read gf grades file and create a new GradeBook. This GradeBook will
        have dict_key as its dictionary key.

        '''

        lines = infile.readlines()
        sep = lines.index('\n')

        header = lines[:sep + 1]
        assts, outofs = _make_out_of_from_gf_header(header)

        stnum_to_student_grades = {}  # gf files are by student number
        stnum_to_comment = {}
        for line in lines[sep + 1:]:
            student = Student.make_student_from_gf_line(line)
            if not student:  # this is a comment/individual formula line
                stnum, comment = _make_comment_from_gf_line(line)
                stnum_to_comment[stnum] = comment
                continue

            grades = Grades.make_grades_from_gf_line(line, assts)
            stnum_to_student_grades[student.student_number] = (student, grades)

        gradebook = GradeBook(stnum_to_student_grades, 'student_number', outofs,
                              stnum_to_comment)

        gradebook.to_key(dict_key)
        return gradebook

    def to_key(self, key):
        '''Convert this Gradebook's dictionaries of student_grades and
        comments to have the new key.'''

        if key == self.dict_key:
            return

        dict_key_to_student_grades = {}
        dict_key_to_comments = {}

        for old_key, (student, grades) in self.studentgrades.items():
            try:
                new_key = getattr(student, key)
            except AttributeError:
                print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                    key, student))
                continue
            dict_key_to_student_grades[new_key] = (student, grades)
            dict_key_to_comments[new_key] = self.comments[old_key]
        self.studentgrades = dict_key_to_student_grades
        self.comments = dict_key_to_comments

    def write_gf(self, outfile, outofs=None, utorid=True, key=default_student_sort):
        '''Write a gf file to outfile.

        outofs is an iterable of asst names: the order in which they will appear in the gf
          If outofs is None, the order will be alphabetical.
        utorid: Include a field for utorid?
        '''

        if outofs is None:
            outofs = sorted(self.outofs.items(), key=lambda pair: pair[0])
        else:
            try:
                outofs = [(asst, self.outofs[asst]) for asst in outofs]
            except KeyError as error:
                raise KeyError(
                    'Invalid assignment list {}: {}'.format(outofs, error))

        header = _make_gf_header(outofs, utorid)
        outfile.write(header + '\n')

        student_grades_list = _sorted_student_grades(self.studentgrades, key)
        for student, grades in student_grades_list:
            comment = self.comments.get(getattr(student, self.dict_key), '')
            line = _make_gf_student_line(
                student, utorid, grades, outofs, comment)
            outfile.write(line)

    def write_csv_submit_file(self, outfile, asst='all', exam_no_shows=None, attribute='student_number'):
        '''Write a CSV submit file for eMarks to outfile.

        asst is the name of the "final mark" assignment
        exam_no_shows is an iterable of values of attribute of Student's

        '''

        if exam_no_shows is None:
            exam_no_shows = []

        for student, grades in self.studentgrades.values():
            try:
                grade = grades.get_grade(asst)
            except KeyError:
                print('WARNING: No grade for assignment {} for this student:\n\t{}'.format(
                    asst, student))
                continue

            no_show = getattr(student, attribute) in exam_no_shows
            outfile.write('{},{}{}\n'.format(student.student_number,
                                             # submit file needs integers
                                             min(math.ceil(grade), 100),
                                             ',y' if no_show else ''))


class Grades:
    '''Essentially a dictionary of grades.'''

    def __init__(self):
        self.grades = {}

    def __iter__(self):
        return iter(self.grades)

    def add_grade(self, assignment, grade=0):
        '''Add/update grade for assignment. Raise TypeError if assignment is
        not a str or if grade cannot be converted to float.

        '''

        grade = _clean_grade(grade)
        assignment = _clean_asst(assignment)
        self.grades[assignment] = grade

    def add_grades(self, grades):
        '''Add/update grades from dictionary grades.

        '''

        for assignment, grade in grades:
            self.add_grade(assignment, grade)

    def get_grade(self, assignment):
        '''Return the grade for assignment. Raise KeyError if no such
        assignment.

        '''

        try:
            return self.grades[assignment]
        except KeyError:
            raise KeyError('No such assignment: {}'.format(assignment))

    @staticmethod
    def make_grades_from_quercus_row(row):
        '''Create and return a Grades from a row of Quercus file.

        '''

        grades = Grades()
        for asst, grade in row.items():
            asst = _clean_asst(asst)
            if isinstance(grade, str) and grade.strip() == '':
                grade = 0
            if _is_quercus_asst_name(asst):
                grades.add_grade(asst, _clean_grade(grade))
        return grades

    @staticmethod
    def make_grades_from_gf_line(line, assts):
        '''Create Grades from a line in a gf file. Return None if line does
        not contain student grades (e.g., it is a comment or header line.)

        '''

        fields = line.strip().split(',')
        match = re.fullmatch(
            r'(\d+) [ dx][ dx] ([\w-]+)((\s+([\w-]+))+)', fields[0])

        # this is not a gf line with student information
        if match is None:
            return None

        grades = Grades()

        if len(fields) == 1:
            return grades

        if not fields[1].isdigit():  # line contains utorid
            fields = fields[2:]
        else:
            fields = fields[1:]

        grades.add_grades(zip(assts, fields))
        return grades

    def to_json(self):
        '''Return a JSON of the grades.'''

        return json.dumps(self.grades, sort_keys=True, indent=4)

    def __str__(self):
        return str(self.grades)


def _clean_grade(grade):
    try:
        return float(grade)
    except ValueError:
        raise TypeError('Invalid type for grade: {} of type {}.'.format(
            grade, type(grade)))


def _clean_asst(assignment):
    if isinstance(assignment, str):
        return assignment.strip()
    raise TypeError('Invalid type for assignment: {} of type {}.'.format(
        assignment, type(assignment)))


def _is_quercus_asst_name(word):
    # assignments on Quercus are "AsstName (numericID)"

    match = re.fullmatch(r'\w+\s\(\d+\)', word.strip())
    return match is not None


def _make_out_of_from_quercus_row(row):
    '''Create and return a dict mapping asst name to total points from a
    row in a quercus gradebook file.

    '''

    outofs = {}
    for key, value in row.items():
        key = _clean_asst(key)
        if _is_quercus_asst_name(key):
            outofs[key] = _clean_grade(value)
    return outofs


def _make_out_of_from_gf_header(header):
    # TODO FIX collecting calculated grades
    outofs = {}
    assts = []
    for line in header:
        match = re.fullmatch(r'(\w+)\s*/\s*(\d+)\n', line)
        if match:
            asst = _clean_asst(match.group(1))
            outof = _clean_grade(match.group(2))
            outofs[asst] = outof
            assts.append(asst)
            continue
        match = re.match(r'(\w+)\s*=', line)  # calculated grade
        if match:
            asst = _clean_asst(match.group(1))
            outof = DEFAULT_FORMULA_OUTOF
            outofs[asst] = outof
            assts.append(asst)
            continue
    return (assts, outofs)


def _make_comment_from_gf_line(line):
    match = re.fullmatch(r'(\d+)[*]\s+(.+)', line.strip())
    if match:
        return match.group(1), match.group(2)
    return None


def _contains_student_data_quercus(row):
    '''Does this row contain student info?'''

    names = row['Student']
    return (names is not None and
            names.strip() != '' and
            names.strip() != 'Points Possible' and
            names.strip() != 'Student, Test')


def _sorted_student_grades(stnum_to_student_grades, key=default_student_sort):
    student_grades_list = list(stnum_to_student_grades.values())

    def sort_key(record):  # sort by student, according to key
        return key(record[0])

    student_grades_list.sort(key=sort_key)
    return student_grades_list


# loaded = GradeBook.load_quercus_grades_file(open('quercus.csv'))
# loaded.write_gf(open('grades.gf', 'w'), [
#                'Exercises (337442)', 'Midtem (337441)', 'Project (337474)'])
loaded = GradeBook.load_gf_file(open('grades.gf'))
# loaded.write_gf(open('new_grades.gf', 'w'), [
#                'Midtem__337441_', 'Project__337474_', 'Exercises__337442_'])
loaded.write_csv_submit_file(open('submit.csv', 'w'), 'all', [
                             '1003336320', '0999617856'])

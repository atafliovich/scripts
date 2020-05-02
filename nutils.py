"""A new set of utilities to work with MarkUs, Quercus, Intranet, CDF
grades files, CATME files, and what not.

"""

import csv
import re
from email_validator import validate_email, EmailNotValidError


MAX_UTORID_LENGTH = 8
STUDENT_NUMBER_LENGTH = 10
DEFAULT_STUDENT_STR = ('last', 'first', 'student_number', 'utorid',
                       'gitid', 'email', 'lecture', 'tutorial', 'id1', 'id2')


def DEFAULT_STUDENT_SORT(student): return student.last + student.first


def make_classlist(students, outfile, attrs=DEFAULT_STUDENT_STR,
                   header=False, key=DEFAULT_STUDENT_SORT):
    '''Write out a CSV classlist to outfile.

    students is the Students object to write.
    outfile is the file to write to, open for writing.
    attrs is an iterable of attributes of Student to include.
    key is the key for sorting Students.
    header is True/False: whether to write the header
    '''

    student_list = list(students)
    student_list.sort(key=key)
    if header:
        outfile.write(','.join(list(attrs)) + '\n')
    for student in student_list:
        outfile.write(student.full_str(attrs) + '\n')


def load_quercus_grades_file(infile, dict_key='student_number'):
    '''Read Quercus CSV Gradebook.
    Return (Dict[dict_key, Tuple(Student, Grades)], outofs).
    The default dictionary key is student_number. Another common use case would be 'utorid'.
    '''

    reader = csv.DictReader(infile)
    dict_key_to_student_grades = {}

    for row in reader:
        first = row['Student'].strip()
        if first in ('', 'Student, Test'):
            continue
        if first == 'Points Possible':
            outofs = _make_out_of_from_quercus_row(row)
            continue

        student = _make_student_from_quercus_row(row)
        grades = _make_grades_from_quercus_row(row)

        try:
            key = getattr(student, dict_key)
            dict_key_to_student_grades[key] = (student, grades)
        except AttributeError:
            print('WARNING: This student does not have attribute {}:\n\t{}'.format(
                dict_key, student))

    return (dict_key_to_student_grades, outofs)


class Students:
    '''A collection of Students.'''

    def __init__(self, iterable=None):
        '''Initialize Students from iterable.'''

        if iterable:
            self.students = set(iterable)
        else:
            self.students = set()

    def add_student(self, student):
        '''Add new student.'''

        self.students.add(student)

    @staticmethod
    def load_intranet_classlist(infile):
        '''Return a new Students created from an Intranet classlist csv file.'''

        reader = csv.DictReader(infile)
        students = set()
        for row in reader:
            names = row['My Students (Lname, Fname)'].split(',')
            student = Student(student_number=row['StudentID'],
                              email=row['Email'],
                              first=names[1],
                              last=names[0],
                              lecture=row['Lecture'],
                              tutorial=row['Tutorial']
                              )
            students.add(student)
        return Students(students)

    @staticmethod
    def load_quercus_classlist(infile):
        '''Return a new Students created from a Quercus possibly empty gradebook
        csv file.'''

        reader = csv.DictReader(infile)
        students = set()
        for row in reader:
            if not _contains_student_data_quercus(row):
                continue
            student = _make_student_from_quercus_row(row)
            students.add(student)

        return Students(students)

    def __iter__(self):
        '''Return an Iterator over these Students.'''

        return iter(self.students)

    def by_utorid(self):
        '''Return a Dict[UTORID, Student]. Raises AttributeError if there is a
        Student with no utorid.'''

        return self._by_field('utorid')

    def by_student_number(self):
        '''Return a Dict[student_number, Student]. Raises AttributeError if there is a
        Student with no student_number.'''

        return self._by_field('student_number')

    def by_gitid(self):
        '''Return a Dict[gitid, Student]. Raises AttributeError if there is a
        Student with no gitid.'''

        return self._by_field('gitid')

    def _by_field(self, field):
        '''Return a Dict[field, Student].  Raises AttributeError if there is
        no attribute field in any of the Students.

        '''

        field2student = {}
        for student in self.students:
            attr = getattr(student, field)
            if attr is not None:
                field2student[attr] = student
            else:
                print('WARNING: This student\'s attribute {} is None!\n\t{}'.format(
                    field, student))
        return field2student

    def full_str(self, ordering=DEFAULT_STUDENT_STR, key=DEFAULT_STUDENT_SORT):
        '''Return a customized str representation of these Students.
        ordering is the other of Student attributes,
        key is the key for sorting Students.
        '''

        student_list = list(self.students)
        student_list.sort(key=key)
        return ('{' + str([student.full_str(ordering)
                           for student in student_list])[1:-1] + '}')

    def __str__(self):
        '''Return a default str representation of these Students.
        '''

        return self.full_str(DEFAULT_STUDENT_STR, DEFAULT_STUDENT_SORT)


class Student:
    """A representation of a student.
    """

    def __init__(self, **kwargs):
        """Instantiate this Student from given fields.
        """

        self.utorid = _clean(kwargs.get('utorid'))
        if self.utorid is not None and not _is_utorid(self.utorid):
            raise InvalidStudentInfoError('UTORID', self.utorid)

        self.student_number = _clean(kwargs.get('student_number'))
        if self.student_number is not None:
            if _is_student_number(self.student_number):
                self.student_number = self.student_number.zfill(10)
            else:
                raise InvalidStudentInfoError(
                    'student number', self.student_number)

        self.email = _clean(kwargs.get('email'))
        if self.email is not None and not _is_email(self.email):
            raise InvalidStudentInfoError('email', self.email)

        self.first = _clean(kwargs.get('first'))
        self.last = _clean(kwargs.get('last'))
        self.lecture = _clean(kwargs.get('lecture'))
        self.tutorial = _clean(kwargs.get('tutorial'))
        self.gitid = _clean(kwargs.get('gitid'))
        self.id1 = _clean(kwargs.get('id1'))
        self.id2 = _clean(kwargs.get('id2'))

    def __str__(self):
        '''Return the default str representation on this Student.'''

        return self.full_str(DEFAULT_STUDENT_STR)

    def full_str(self, ordering=DEFAULT_STUDENT_STR):
        '''Return a customized str representation of this Student.
        ordering is the other of Student attributes.
        '''

        attrs = []
        for attr_name in ordering:
            attr = getattr(self, attr_name)
            if attr:
                attrs.append(attr)
        return ','.join(attrs)


class Grades:
    '''Essentially a dictionary of grades.'''

    def __init__(self):
        self.grades = {}

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


def _make_student_from_quercus_row(row):
    '''Create and return a Student from a row of Quercus file.'''

    names = row['Student'].split(',')
    sections = row['Section'].split(' and ')
    student = Student(student_number=row['Integration ID'],
                      utorid=row['SIS User ID'],
                      first=names[1],
                      last=names[0],
                      lecture=sections[0],
                      tutorial=sections[1],
                      id1=row['ID']
                      )
    return student


def _make_grades_from_quercus_row(row):
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


def _make_out_of_from_quercus_row(row):
    '''Create and return a dict mapping asst name to total points.'''

    outofs = {}
    for key, value in row.items():
        key = _clean_asst(key)
        if _is_quercus_asst_name(key):
            outofs[key] = _clean_grade(value)
    return outofs


def _is_quercus_asst_name(word):
    # assignments on Quercus are "AsstName (numericID)"

    match = re.fullmatch(r'\w+\s\(\d+\)', word.strip())
    return match is not None


def _clean(word):
    return word.strip() if word else word


def _is_utorid(word):
    '''Alphanumeric up to MAX_UTORID_LENGTH.'''

    return word.isalnum() and len(word) <= MAX_UTORID_LENGTH


def _is_student_number(word):
    return (word.isdigit() and
            STUDENT_NUMBER_LENGTH - 1 <= len(word) <= STUDENT_NUMBER_LENGTH)


def _is_email(word):
    try:
        validate_email(word)
    except EmailNotValidError:
        return False
    return True


def _contains_student_data_quercus(row):
    '''Does this row contain student info?'''

    names = row['Student']
    return (names is not None and
            names.strip() != '' and
            names.strip() != 'Points Possible' and
            names.strip() != 'Student, Test')


class InvalidStudentInfoError(Exception):
    '''Exception raised on attempt to create Student with invalid fields.
    '''

    def __init__(self, field, value):
        '''field: name of kwarg that is invalid
        value: value of kwarg that is invalid'''

        Exception.__init__(self)
        self.message = 'Cannot create Student with given {}: {}.'.format(
            field, value)

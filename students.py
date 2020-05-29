'''Representations of a single Student and a bunch of Students.'''


import csv
import json
import re
from email_validator import validate_email, EmailNotValidError


from defaults import (DEFAULT_STUDENT_STR, default_student_sort,
                      MAX_UTORID_LENGTH, STUDENT_NUMBER_LENGTH)
from shared import _make_gf_header, _make_gf_student_line

# two Student's are equal if they match on any of these attributes
EQ_STUDENTS = ('student_number', 'utorid', 'gitid')


class Students:
    '''Students hashed by some dict_key.'''

    def __init__(self, iterable=None, dict_key='student_number'):
        '''Initialize Students from iterable.'''

        if iterable:
            self.students = dict(
                (getattr(student, dict_key), student) for student in iterable)
        else:
            self.students = {}
        self.dict_key = dict_key

    def add_student(self, student):
        '''Add new student.'''

        self.students[getattr(student, self.dict_key)] = student

    @staticmethod
    def load_intranet_classlist(infile, dict_key='student_number'):
        '''Return a new Students created from an Intranet classlist csv file.'''

        reader = csv.DictReader(infile)
        students = Students(None, dict_key)
        for row in reader:
            names = row['My Students (Lname, Fname)'].split(',')
            student = Student(student_number=row['StudentID'],
                              email=row['Email'],
                              first=names[1],
                              last=names[0],
                              lecture=row['Lecture'],
                              tutorial=row['Tutorial']
                              )
            students.add_student(student)
        return students

    @staticmethod
    def load_quercus_classlist(infile, dict_key='student_number'):
        '''Return a new Students created from a Quercus possibly empty gradebook
        csv file.'''

        reader = csv.DictReader(infile)
        students = Students(None, dict_key)
        for row in reader:
            if not _contains_student_data_quercus(row):
                continue
            student = Student.make_student_from_quercus_row(row)
            students.add_student(student)

        return students

    def __iter__(self):
        '''Return an Iterator over these Students.'''

        return iter(self.students.values())

    @staticmethod
    def load_classlist(infile, attrs=DEFAULT_STUDENT_STR,
                       dict_key='student_number'):
        '''Return a new Students created from a classlist csv file.  attrs
        correspond to the columns in the classlist file.

        '''

        reader = csv.reader(infile)
        students = Students(None, dict_key)
        for row in reader:
            student = Student(**dict(zip(attrs, row)))
            students.add_student(student)
        return students

    def write_classlist(self, outfile,
                        attrs=DEFAULT_STUDENT_STR, header=False,
                        key=default_student_sort):
        '''Write out a CSV classlist to outfile.

        outfile is the file to write to, open for writing.
        attrs is an iterable of attributes of Student to include.
        key is the key for sorting Students.
        header is True/False: whether to write the header
        '''

        student_list = list(self.students.values())
        student_list.sort(key=key)
        if header:
            outfile.write(','.join(list(attrs)) + '\n')
        for student in student_list:
            outfile.write(student.full_str(attrs) + '\n')

    def write_gf(self, outfile, outofs=None, utorid=True,
                 key=default_student_sort):
        '''Write out an empty gf file.

        outfile is the file to write to, open for writing.
        outofs is a Dict[asst:str, outof:int] for the header.
        key is the key for sorting Students.
        utorid is True/False: whether to include utorids.
        '''

        if outofs is None:
            outofs = {}

        student_list = list(self.students.values())
        student_list.sort(key=key)

        header = _make_gf_header(outofs, utorid)
        outfile.write(header + '\n')

        for student in student_list:
            line = _make_gf_student_line(student, utorid)
            outfile.write(line)

    def by_utorid(self):
        '''Return a Dict[utorid, Student]. Raises AttributeError if there is a
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

    def _by_field(self, attribute):
        '''Return a Dict[attribute, Student].  Raises AttributeError if there
        is no such attribute in one (or more) Student.

        '''

        attr2student = {}
        for student in self.students.values():
            attr = getattr(student, attribute)
            if attr is not None:
                attr2student[attr] = student
            else:
                print('WARNING: This student\'s attribute {} is None!\n\t{}'.format(
                    attribute, student))
        return attr2student

    def to_json(self):
        '''Return a JSON for these Students.'''

        return '{{ {} }}'.format(','.join([student.to_json() for student in self.students]))

    def full_str(self, ordering=DEFAULT_STUDENT_STR, key=default_student_sort):
        '''Return a customized str representation of these Students.
        ordering is the other of Student attributes,
        key is the key for sorting Students.
        '''

        student_list = list(self.students.values())
        student_list.sort(key=key)
        return ('{' + str([student.full_str(ordering)
                           for student in student_list])[1:-1] + '}')

    def __len__(self):
        return len(self.students)

    def __str__(self):

        return self.full_str(DEFAULT_STUDENT_STR, default_student_sort)

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(student in other for student in self.students.values()))


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

    def to_json(self):
        '''Return a JSON for this Student: all attributes.'''
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):

        return self.full_str(DEFAULT_STUDENT_STR)

    def __eq__(self, other):
        result = any(getattr(self, attr) and (getattr(self, attr) == getattr(other, attr))
                     for attr in EQ_STUDENTS)
        return result

    def full_str(self, attrs=DEFAULT_STUDENT_STR):
        '''Return a customized str representation of this Student.
        attrs is an iterable of Student attributes to include, in order.
        '''

        return ','.join([getattr(self, attr) if getattr(self, attr) else ''
                         for attr in attrs])

    @staticmethod
    def make_student_from_gf_line(line):
        '''Create a Student from line from a gf file. Return None on a line
        that does not contain student information.'''

        fields = line.strip().split(',')
        match = re.fullmatch(
            r'(\d+) [ dx][ dx] ([^,]+)((\s+([^,]+))+)', fields[0])

        # this is not a gf line with student information (e.g., a comment line)
        if match is None:
            return None

        stunum = match.group(1)
        last = match.group(2)
        first = match.group(3).strip()
        utorid = fields[1] if len(
            fields) > 1 and not fields[1].isdigit() else None

        return Student(student_number=stunum, first=first, last=last, utorid=utorid)

    @staticmethod
    def make_student_from_quercus_row(row):
        '''Create and return a Student from a row of Quercus file. Return None if row
        does not contain student data.

        '''

        if not _contains_student_data_quercus(row):
            return None

        names = row['Student'].split(',')
        sections = row['Section'].split(' and ')
        student = Student(student_number=row['Integration ID'],
                          utorid=row['SIS User ID'],
                          first=names[1],
                          last=names[0],
                          lecture=sections[0],
                          tutorial=sections[1] if len(sections) > 1 else '',
                          id1=row['ID'])
        return student


class InvalidStudentInfoError(Exception):
    '''Exception raised on attempt to create Student with invalid fields.
    '''

    def __init__(self, attribute, value):
        '''attribute: name of invalid attribute
        value: value of invalid attribute
        '''

        Exception.__init__(self)
        self.message = 'Cannot create Student with given {}: {}.'.format(
            attribute, value)


def _contains_student_data_quercus(row):
    '''Does this row contain student info?'''

    names = row['Student']
    return (names is not None and
            names.strip() != '' and
            names.strip() != 'Points Possible' and
            names.strip() != 'Student, Test')


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

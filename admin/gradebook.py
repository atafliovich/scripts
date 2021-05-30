"""My gradebook."""

import json
import math
import re

from .defaults import default_student_sort, DEFAULT_FORMULA_OUTOF
from .shared import _make_gf_header, _make_gf_student_line, _make_csv_header
from .students import Student, Students

SEARCH_BY = ('student_number', 'utorid', 'gitid')

DEBUG = True


class GradeBook:
    """My own gradebook."""

    def __init__(self, studentgrades=None, dict_key='student_number',
                 outofs=None, comments=None, sanity_check=True):
        """Init a Gradesfile given:

        outofs: Dict[str, float] maps assigment name to max possible grade.
        dict_key: a Student attribute; key into studentgrades and comments.
           Most likely student_number or utorid.
        studentgrades: Dict[dict_key, Tuple(Student, Grades)].
        comments: Dict[dict_key, str].
        sanity_check: check created GradeBook for inconsistencies or errors?

        """

        self.outofs = dict(outofs) if outofs else {}
        self.studentgrades = dict(studentgrades) if studentgrades else {}
        self.dict_key = dict_key
        self.comments = dict(comments) if comments else {}
        if sanity_check:
            self.sanity_check()

    def sanity_check(self):
        """Check validity of this GradeBook."""

        try:
            _validate(self.studentgrades, self.dict_key,
                      self.outofs, self.comments)
        except AssertionError as error:
            print('WARNING: Invalid GradeBook. {}'.format(error))
            return False
        return True

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

    def __len__(self):
        return len(self.studentgrades)

    def __eq__(self, other):

        if len(self.studentgrades) != len(other.studentgrades):
            return False

        if self.outofs != other.outofs:
            return False

        for (student, grades) in self.studentgrades.values():
            search_attrs = dict(
                (attr, getattr(student, attr))
                for attr in SEARCH_BY if getattr(student, attr) is not None)
            other_record = other.get_student_info(search_attrs)
            if not other_record:
                return False
            if grades != other_record[1]:
                if DEBUG:
                    print('different grades for {}: {} vs {}'.format(
                        student, grades, other_record[1]))
                return False
        return True

    def get_student_info(self, search_by):
        """search_by is a Dict[attribute, attr_value]. Return (Student,
        Grades) if a Student matches any of the search_by, or None if
        no such Student."""

        for student, grades in self.studentgrades.values():
            if any(getattr(student, attribute) == attr_value
                   for attribute, attr_value in search_by.items()):
                return (student, grades)
        return None

    def get_students(self):
        """Return a Students object with this Gradebook' students."""

        return Students(record[0] for record in self.studentgrades.values())

    def get_student_grades_by_utorid(self, utorid):
        """Return Grades of a Student with utorid. Raise NoSuch? if no such
        Student."""

        return self.get_student_grades_by_attribute('utorid', utorid)

    def get_student_grades_by_student_number(self, student_number):
        """Return Grades of a Student with student_number. Raise NoSuch? if no
        such Student."""

        return self.get_student_grades_by_attribute('student_number',
                                                    student_number)

    def get_student_grades_by_attribute(self, attribute, attr_value):
        """Return Grades of a Student with value of attribute equal to
        attr_value.  Raise NoSuch? if no such Student. Raise
        AttributeError if attribute is not present in at least one
        Student.

        """

        for student, grades in self.studentgrades.values():
            if getattr(student, attribute) == attr_value:
                return grades
        raise Exception('No student with {} value {}.'.format(
            attribute, attr_value))

    def get_dict(self, key):
        """Return a Dict[key, Tuple(Student, Grades).

        Useful when self.key = 'student_number' and we want the dict
        by 'utorid', for example.

        """

        if key == self.dict_key:
            return self.studentgrades

        new_key_to_student_grades = {}
        for student, grades in self.studentgrades.values():
            try:
                key = getattr(student, key)
                new_key_to_student_grades[key] = (student, grades)
            except AttributeError:
                print('WARNING: '
                      'Student does not have attribute {}:\n\t{}'.format(
                          key, student))
        return new_key_to_student_grades

    @staticmethod
    def load_gf_file(infile, dict_key='student_number', use_utorid=True):
        """Read gf grades file and create a new GradeBook. This GradeBook will
        have dict_key as its dictionary key.

        """

        lines = infile.readlines()
        sep = lines.index('\n')

        header = lines[:sep + 1]
        assts, outofs = _make_out_of_from_gf_header(header)

        stnum_to_student_grades = {}  # gf files are by student number
        stnum_to_comment = {}
        for line in lines[sep + 1:]:
            student = Student.make_student_from_gf_line(line, use_utorid)
            if not student:  # this is a comment/individual formula line
                stnum, comment = _make_comment_from_gf_line(line)
                stnum_to_comment[stnum] = comment
                continue

            grades = Grades.make_grades_from_gf_line(line, assts)
            stnum_to_student_grades[student.student_number] = (student, grades)

        gradebook = GradeBook(stnum_to_student_grades,
                              'student_number', outofs,
                              stnum_to_comment)

        gradebook.to_key(dict_key)
        return gradebook

    def to_key(self, key):
        """Convert this Gradebook's dictionaries of student_grades and
        comments to have the new key."""

        if key == self.dict_key:
            return

        dict_key_to_student_grades = {}
        dict_key_to_comments = {}

        for old_key, (student, grades) in self.studentgrades.items():
            try:
                new_key = getattr(student, key)
            except AttributeError:
                print('WARNING: '
                      'Student does not have attribute {}:\n\t{}'.format(
                          key, student))
                continue
            dict_key_to_student_grades[new_key] = (student, grades)
            if old_key in self.comments:
                dict_key_to_comments[new_key] = self.comments[old_key]
        self.studentgrades = dict_key_to_student_grades
        self.comments = dict_key_to_comments
        self.dict_key = key

    def write_gf(self, outfile, assts=None, utorid=True,
                 key=default_student_sort):
        """Write a gf file to outfile.

        assts is an iterable of asst names: the order in which they
        will appear in the gf.  If assts is None, the order will be
        alphabetical and all grades will be included.  utorid: Include
        a field for utorid?

        """

        outofs = _sort_outofs(self.outofs, assts)
        header = _make_gf_header(outofs, utorid)
        outfile.write(header + '\n')

        student_grades_list = _sorted_student_grades(self.studentgrades, key)
        for student, grades in student_grades_list:
            comment = self.comments.get(getattr(student, self.dict_key), '')
            line = _make_gf_student_line(
                student, utorid, grades, outofs, comment)
            outfile.write(line)

    def get_grades_dict(self, asst, key='student_number'):
        """Return Dict[key, grade:float] of grades for assignment asst.

        asst is the assignment name for which the grades will be collected.
        """

        return {getattr(student, key):
                self.get_student_grades_by_student_number(
                    student.student_number).get_grade(asst)
                for student in self.get_students()}

    def write_csv_grades_file(self, outfile, student_attrs=None,
                              header=True, comments=True, assts=None,
                              key=default_student_sort, names=None):
        """Write a csv grades file to outfile.

        student_attrs is an iterable of Student attributes to be
           included in the file, in the order in which they will
           appear.
        assts is an iterable of asst names: the order in which they
          will appear in the gf.  If assts is None, the order will be
          alphabetical and all grades will be included.
        comments: include comments as a last column?
        names is Dict[asst-or-attr, new-name] specifies how the header
           is created, in case we want it to be different from just
           the names of Student attributes and assignment names as
           stored. One of the keys can be 'comments' to replace the
           word 'comments' in the header.

        """

        if student_attrs is None:
            student_attrs = []
        if assts is None:
            assts = []

        if header:
            outfile.write(_make_csv_header(
                student_attrs, assts, comments, names))

        student_grades_list = _sorted_student_grades(self.studentgrades, key)
        for student, grades in student_grades_list:
            student_grades = ''.join(
                [',{}'.format(grades.get_grade(asst)) for asst in assts])
            student_comment = (',{}'.format(self.comments.get(
                getattr(student, self.dict_key), '')) if comments else '')
            outfile.write('{}{}{}\n'.format(
                student.full_str(student_attrs),
                student_grades,
                student_comment))

    def write_csv_submit_file(self, outfile, asst='all',
                              exam_no_shows=None, attribute='student_number'):
        """Write a CSV submit file for eMarks to outfile.

        asst is the name of the "final mark" assignment
        exam_no_shows is an iterable of values of attribute of Student's

        """

        if exam_no_shows is None:
            exam_no_shows = []

        for student, grades in self.studentgrades.values():
            try:
                grade = grades.get_grade(asst)
            except KeyError:
                print('WARNING: '
                      'No grade for assignment {} for student:\n\t{}'.format(
                          asst, student))
                continue

            no_show = getattr(student, attribute) in exam_no_shows
            outfile.write('{},{}{}\n'.format(student.student_number,
                                             # submit file needs integers
                                             min(math.ceil(grade), 100),
                                             ',y' if no_show else ''))


class Grades:
    """Essentially a dictionary of grades."""

    def __init__(self, grades=None):
        self.grades = {}
        if grades:
            for asst, grade in grades.items():
                self.add_grade(asst, grade)

    def __iter__(self):
        return iter(self.grades)

    def add_grade(self, assignment, grade=0):
        """Add/update grade for assignment. Raise TypeError if assignment is
        not a str or if grade cannot be converted to float.

        """

        grade = _clean_grade(grade)
        assignment = _clean_asst(assignment)
        self.grades[assignment] = grade

    def add_grades(self, grades):
        """Add/update grades from dictionary grades.

        """

        for assignment, grade in grades:
            self.add_grade(assignment, grade)

    def get_grade(self, assignment):
        """Return the grade for assignment. Raise KeyError if no such
        assignment.

        """

        try:
            return self.grades[assignment]
        except KeyError:
            raise KeyError('No such assignment: {}'.format(assignment))

    def get_assignments(self):
        """Return a set of assignments in these Grades."""

        return set(self.grades.keys())

    @staticmethod
    def make_grades_from_gf_line(line, assts):
        """Create Grades from a line in a gf file. Return None if line does
        not contain student grades (e.g., it is a comment or header line.)

        """

        fields = line.strip().split(',')
        match = re.fullmatch(
            r'(\d+) [ dx][ dx] ([^,]+)((\s+([^,]+))+)', fields[0])

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

        # pad with zeros for missing grades
        grades.add_grades(
            zip(assts, fields + [0] * (len(assts) - len(fields))))
        return grades

    def to_json(self):
        """Return a JSON of the grades."""

        return json.dumps(self.grades, sort_keys=True, indent=4)

    def __str__(self):
        return str(self.grades)

    def __eq__(self, other):

        if other is None:
            return False

        for asst, grade in self.grades.items():
            if asst not in other.grades:
                return False
            if not grades_equal(grade, other.grades[asst]):
                return False
        return True


def _clean_grade(grade):
    if grade == '' or str(grade).lower() == 'gwr':
        return 0.0
    try:
        return float(grade)
    except ValueError:
        raise TypeError('Invalid type for grade: {} of type {}.'.format(
            grade, type(grade)))


def _clean_asst(assignment):
    if not isinstance(assignment, str):
        raise TypeError('Invalid type for assignment: {} of type {}.'.format(
            assignment, type(assignment)))

    return assignment.strip()


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


def _sort_outofs(outofs, asst_order):
    """Return a List[(asst, outof)] in the order in which asstignments
    appear in asst_order. If asst_order is None, sort in alphabetical
    order.
    outofs is a Dict{asst, outof}
    """

    if asst_order is None:
        result = sorted(outofs.items(), key=lambda pair: pair[0])
    else:
        try:
            result = [(asst, outofs[asst]) for asst in asst_order]
        except KeyError as error:
            raise KeyError(
                'Invalid assignment list {}: {}'.format(outofs, error))
    return result


def _sorted_student_grades(stnum_to_student_grades, key=default_student_sort):
    student_grades_list = list(stnum_to_student_grades.values())

    def sort_key(record):  # sort by student, according to key
        return key(record[0])

    student_grades_list.sort(key=sort_key)
    return student_grades_list


def _validate(student_grades, dict_key, outofs, comments):

    for key, (student, grades) in student_grades.items():
        assert getattr(student, dict_key) == key
        assert grades is None or grades.get_assignments() == outofs.keys()

    assert all(key in student_grades for key in comments)


def grades_equal(grade1, grade2):
    """Return whether grade1 and grade2 are the same grade, with 0.1
    precision."""

    return round(grade1, 1) == round(grade2, 1)

'''Test values for testing GradeBook.'''

import re
import sys
import unittest

from gradebook import GradeBook, Grades
from students import Student

astudent = {'last': 'Alastname', 'first': 'Afirstname',
            'utorid': 'aaaaaaaa', 'student_number': '1003336320'}
bstudent = {'last': 'Blast-name', 'first': 'Bfirstname',
            'utorid': 'bbbbbbbb', 'student_number': '1003253249'}
cstudent = {'last': 'Clastname', 'first': 'Cfirst Cname',
            'utorid': 'cccccccc', 'student_number': '0999617856'}
dstudent = {'last': 'Dl', 'first': 'Df Df-Dff',
            'utorid': 'dddddddd', 'student_number': '1001591690'}
estudent = {'last': 'Elastname', 'first': 'E.E.',
            'utorid': 'eeeeeeee', 'student_number': '1006631129'}
fstudent = {'last': 'Flastname', 'first': 'F. Ff.',
            'utorid': 'ffffffff', 'student_number': '999030141'}
gstudent = {'last': 'Glast', 'first': 'G-gfirst',
            'utorid': 'gggg1234', 'student_number': '999020820'}
hstudent = {'last': 'HlastMissingGrade', 'first': 'Hfirst', 'utorid':
            'hhhhhhhh', 'student_number': '1003511078'}

agrades = {'Exam': 62.64, 'Midtem': 24, 'Exercises': 14, 'Project':
           50, 'NewGradeNoNum': 50}
bgrades = {'Exam': 24.44, 'Midtem': 26, 'Exercises': 11, 'Project':
           52, 'NewGradeNoNum': 52}
cgrades = {'Exam': 53.87, 'Midtem': 24, 'Exercises': 13, 'Project':
           50.2, 'NewGradeNoNum': 50}
dgrades = {'Exam': 60.97, 'Midtem': 15, 'Exercises': 14, 'Project':
           44.8, 'NewGradeNoNum': 51}
egrades = {'Exam': 41.37, 'Midtem': 22, 'Exercises': 5, 'Project':
           43.3, 'NewGradeNoNum': 53}
fgrades = {'Exam': 50.84, 'Midtem': 23, 'Exercises': 14, 'Project':
           32.8, 'NewGradeNoNum': 54}
ggrades = {'Exam': 65, 'Midtem': 16, 'Exercises': 14, 'Project': 49,
           'NewGradeNoNum': 55}
hgrades = {'Midtem': 26, 'Project': 50,
           'NewGradeNoNum': 56, 'Exam': 0, 'Exercises': 0}

outofs = {'Exam': 74, 'Midtem': 38, 'Exercises': 15, 'Project': 55,
          'NewGradeNoNum': 55}

comments = {'aaaaaaaa': 'acomment ac comma aac',
            'bbbbbbbb': 'bc',
            'hhhhhhhh': 'hcomm comm comm. ?! " blah '}


def collect_vars(pattern):
    return [getattr(sys.modules[__name__], name)
            for name in dir(sys.modules[__name__]) if re.fullmatch(pattern, name)]


class TestLoadQuercusFile(unittest.TestCase):
    '''Sanity check test for loading a Quercus file.'''

    def setUp(self):
        student_vars = collect_vars(r'[abcdefgh]student')
        grades_vars = collect_vars(r'[abcdefgh]grades')
        students = [Student(**student_var) for student_var in student_vars]
        gradess = [Grades(grades_var) for grades_var in grades_vars]

        studentgrades = dict(
            (student.utorid, (student, grades))
            for student, grades in zip(students, gradess))

        self.gradebook = GradeBook(studentgrades, 'utorid', outofs, comments)

    def test_basic(self):
        '''Simple test.'''

        with open('quercus_test_file.csv') as infile:
            loaded = GradeBook.load_quercus_grades_file(infile, 'utorid')
            self.assertEqual(
                self.gradebook, loaded,
                'Incorrectly loaded Quercus grades file. GradeBooks differ:\n{}{}'.format(
                    self.gradebook, loaded))


if __name__ == '__main__':
    unittest.main()

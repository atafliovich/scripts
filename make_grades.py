'''Create and write a gf file with all grades. Best for CSCA08.'''

from typing import Dict, List, TextIO, Tuple
from utils import Student


STUDENT_NUMBER_INDEX = 0
EXCLUDE = True  # mark exam no-shows with x?


def read_class_list(classlist: TextIO) -> Tuple[Dict[str, Student],
                                                Dict[str, Student]]:
    '''Read a CSV classlist file.'''

    utorid_to_students = {}
    stunum_to_students = {}

    classlist.readline()  # skip header
    for line in classlist:
        last, first, utorid, stunum, email = line.strip().split(',')
        stunum = stunum.zfill(10)  # make sure all stunums are 10 digit
        student = Student(student_id=utorid,
                          student_number=stunum,
                          last=last,
                          first=first,
                          email=email)
        utorid_to_students[utorid] = student
        stunum_to_students[stunum] = student

    return utorid_to_students, stunum_to_students


def read_pcrs_grades(gradesfile: TextIO) -> Dict[str, str]:
    '''Return utorid to PCRS grade dict.
    '''

    lines = (line.strip().split(',') for line in gradesfile)
    return dict((line[0], line[1]) for line in lines)


def read_assts_grades(gradesfile: TextIO) -> Dict[str, List[str]]:
    '''Return utorid to [A1, A2, A3] grades dict.
    '''

    lines = (line.strip().split(',') for line in gradesfile)
    return dict((line[0], line[1:]) for line in lines)


def read_midterm_grades(gradesfile: TextIO) -> Dict[str, str]:
    '''Return student number to midterm grade dict.
    '''

    gradesfile.readline()  # skip header
    lines = (line.strip().split(',') for line in gradesfile)
    return dict((line[0].zfill(10), line[-1]) for line in lines)


def read_exam_grades(gradesfile: TextIO) -> Dict[str, str]:
    '''Return student number to exam grade dict.
    '''

    gradesfile.readline()  # skip header
    lines = (line.strip().split(',') for line in gradesfile)
    return dict((line[0].zfill(10), line[-1]) for line in lines)


def read_latest_stunums(classlist: TextIO) -> List[str]:
    '''Return a list of student numbers from classlist. The idea is that
    this is the latest enrollment file.

    '''

    classlist.readline()
    return [line.strip().split(',')[STUDENT_NUMBER_INDEX].zfill(10)
            for line in classlist]


def compile_grades(stunum_to_students: Dict[str, Student],
                   recent: List[str],
                   utorid_to_pcrs: Dict[str, str],
                   utorid_to_assts: Dict[str, List[str]],
                   stunum_to_midterm: Dict[str, str],
                   stunum_to_exam: Dict[str, str],
                   outfile: TextIO) -> None:
    '''Write to outfile:
    stunum    LastName  FirstName,utorid,pcrs,a1,a2,a3,mid,exam
    Omit records for stunums not in recent.
    '''

    for stnum, student in stunum_to_students.items():
        stnum = stnum.zfill(10)  # make sure all stunums are 10-digit
        if EXCLUDE and (stnum not in stunum_to_exam):
            info = '{}  x {}  {}'.format(stnum, student.last, student.first)
        else:
            info = '{}    {}  {}'.format(stnum, student.last, student.first)
        line = ','.join(
            [info,
             student.student_id,
             utorid_to_pcrs.get(student.student_id, '0'),
             ','.join(utorid_to_assts.get(
                 student.student_id, ['0', '0', '0'])),
             stunum_to_midterm.get(stnum, '0'),
             stunum_to_exam.get(stnum, '0')])

        if stnum in recent:
            outfile.write(line + '\n')


if __name__ == '__main__':

    with open('classlist.csv') as cls:
        UTORID_TO_STUDENTS, STUNUM_TO_STUDENTS = read_class_list(cls)

    with open('pcrs/pcrs.csv') as grs:
        UTORID_TO_PCRS = read_pcrs_grades(grs)

    with open('assts/assts.csv') as grs:
        UTORID_TO_ASSTS = read_assts_grades(grs)

    with open('midterm/midterm.csv') as grs:
        STUNUM_TO_MIDTERM = read_midterm_grades(grs)

    with open('exam/exam.csv') as grs:
        STUNUM_TO_EXAM = read_exam_grades(grs)

    with open('may7_intranet.csv') as cls:
        RECENT = read_latest_stunums(cls)

    with open('all.csv', 'w') as writeto:
        compile_grades(STUNUM_TO_STUDENTS,
                       RECENT,
                       UTORID_TO_PCRS,
                       UTORID_TO_ASSTS,
                       STUNUM_TO_MIDTERM,
                       STUNUM_TO_EXAM,
                       writeto)

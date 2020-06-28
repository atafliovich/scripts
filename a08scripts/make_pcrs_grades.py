'''Script to compile PCRS marks from csv files downloaded from PCRS.
'''

from typing import Dict, List, TextIO

FILES = [("On_Campus-Week_{}:_Prepare-122618.csv".format(i),
          "On_Campus-Week_{}:_Perform-122618.csv".format(i))
         for i in range(2, 11)]

UTORID_INDEX = 0
MC_INDEX = -1
MC_OUT_OF_INDEX = -1
PYTHON_INDEX = -3
PYTHON_OUT_OF_INDEX = -3
OUT_OF_LINE_INDEX = 1
FIRST_GRADE_LINE_INDEX = 3


def read_prepare_grades(csv_file: TextIO) -> Dict[str, float]:
    '''Return a dict which maps utorids to corresponding values from the
    problems_multiple_choice_solved column, scaled to out of 0.5, in the
    grades file for a Prepare exercise csv_file.

    '''

    lines = csv_file.readlines()
    out_of = float(lines[OUT_OF_LINE_INDEX].strip().split(',')
                   [MC_OUT_OF_INDEX])
    table = (row.strip().split(',')
             for row in lines[FIRST_GRADE_LINE_INDEX:])
    utorids_grades = \
        ((row[UTORID_INDEX],
          float(row[MC_INDEX]) * 0.5 / out_of if row[MC_INDEX] else 0.0)
         for row in table)
    return dict(utorids_grades)


def read_perform_grades(csv_file: TextIO) -> Dict[str, float]:
    '''Return a dict which maps utorids to grades, scaled to out of 1,
    based on the information in the grades file for a Perform exercise
    csv_file.

    The grade is calculated as follows:
    (mc + 3 * p) / (mc_out_of + 3 * p_out_of) where mc and p are the
    corresponding values from the problems_multiple_choice_solved and
    problems_python_solved columns, and mc_out_of and p_out_of are the
    corresponding maximum attaintable grades.

    '''

    lines = csv_file.readlines()
    out_of_mc = float(lines[OUT_OF_LINE_INDEX].strip().split(',')
                      [MC_OUT_OF_INDEX])
    out_of_p = float(lines[OUT_OF_LINE_INDEX].strip().split(',')
                     [PYTHON_OUT_OF_INDEX])
    table = (row.strip().split(',')
             for row in lines[FIRST_GRADE_LINE_INDEX:])
    utorids_grades = \
        ((row[UTORID_INDEX],
          ((float(row[MC_INDEX]) if row[MC_INDEX] else 0.0) +
           3 * float(row[PYTHON_INDEX]) if row[PYTHON_INDEX] else 0.0) /
          (out_of_mc + 3 * out_of_p)) for row in table)
    return dict(utorids_grades)


def compile_utorid_to_prepare_grades() -> Dict[str, List[float]]:
    '''Return a dict that maps utorids to a list of grades for all Prepare
    exercises.

    '''

    utorid_to_prepare = {}

    for (grades_file, _) in FILES:
        with open(grades_file) as grf:
            utorid_to_grade = read_prepare_grades(grf)
        for utorid, grade in utorid_to_grade.items():
            utorid_to_prepare[utorid] = (utorid_to_prepare.get(utorid, [])
                                         + [grade])

    return utorid_to_prepare


def compile_utorid_to_perform_grades() -> Dict[str, List[float]]:
    '''Return a dict that maps utorids to a list of grades for all Perform
    exercises.

    '''

    utorid_to_perform = {}

    for (_, grades_file) in FILES:
        with open(grades_file) as grf:
            utorid_to_grade = read_perform_grades(grf)
        for utorid, grade in utorid_to_grade.items():
            utorid_to_perform[utorid] = (utorid_to_perform.get(utorid, [])
                                         + [grade])

    return utorid_to_perform


def calc_pcrs_grades(
        utorid_to_prepare_grades: Dict[str, List[float]],
        utorid_to_perform_grades: Dict[str, List[float]]) -> Dict[str, float]:
    '''Return a dict that maps utorids to calculated PCRS grades given a
    dicts that map utorids to a list of pcrs prepare grades and a list
    of PCRS perform grades, accordingly.

    '''

    # CUSTOMIZED FOR FALL 2018
    utorid_to_pcrs = {}
    for utorid, prepare_grades in utorid_to_prepare_grades.items():
        prepare_grade = 0.5 + sum(prepare_grades) - min(prepare_grades[1:])
        perform_grades = utorid_to_perform_grades[utorid]
        perform_grade = sum(perform_grades) - min(perform_grades)
        utorid_to_pcrs[utorid] = (prepare_grade + perform_grade) * 9 / 8

    return utorid_to_pcrs


if __name__ == '__main__':
    #import pprint

    #pprint.pprint(read_prepare_grades(open("On_Campus-Week_2:_Prepare-122618.csv")))
    #pprint.pprint(read_perform_grades(open("On_Campus-Week_2:_Perform-122618.csv")))
    #pprint.pprint(compile_utorid_to_prepare_grades())
    #pprint.pprint(compile_utorid_to_perform_grades())
    #pprint.pprint(calc_pcrs_grades(compile_utorid_to_prepare_grades(),
    #                               compile_utorid_to_perform_grades()))
    #print(len(calc_pcrs_grades(compile_utorid_to_prepare_grades(),
    #                           compile_utorid_to_perform_grades())))

    with open('pcrs.csv', 'w') as gradesfile:
        gradesfile.write(
            '\n'.join(['{},{}'.format(utorid, grade)
                       for (utorid, grade)
                       in calc_pcrs_grades(
                           compile_utorid_to_prepare_grades(),
                           compile_utorid_to_perform_grades()).items()]))

from typing import TextIO, Dict, List


def read_assts_grades(grades_file: TextIO) -> Dict[str, float]:

    utorid_to_grades = {}
    grades_file.readline()  # skip header
    for line in grades_file:
        line = line.strip().split(',')
        grades = make_asst_grades(line[1:])
        utorid_to_grades[line[0]] = grades
    return utorid_to_grades


def make_asst_grades(raw: List[float]) -> List[float]:
    '''Return a list of [A1, A2, A3] grades, given the list of [A1,
    A1_res, A2, A2_res, A3, A3_res] grades. Resubmission penalty is
    20%. Take maximums.

    '''

    [a1, a1_res, a2, a2_res, a3, a3_res] = [float(value) for value in raw]
    return [max(a1, a1_res * 0.8), max(a2, a2_res * 0.8), max(a3, a3_res * 0.8)]


if __name__ == '__main__':

    with open('assts_raw.csv') as grs:
        UTORID_TO_GRADES = read_assts_grades(grs)

    with open('assts.csv', 'w') as grs:
        grs.write(
            '\n'.join([','.join([utorid] + [str(grade) for grade in grades])
                       for utorid, grades in UTORID_TO_GRADES.items()]))

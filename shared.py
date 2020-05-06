'''Shared helpers for various utils. Probablyu do not use directly.'''


def _make_gf_header(outofs=None, utorid=False):
    '''outofs is a List[(asst, grade)], as it must be ordered for gf.
    utorid: should we include a line for utorid?

    '''

    if outofs is None:
        outofs = []
    header = '*/,\n'
    if utorid:
        header = header + 'utorid " ! , 9\n'
    for asst, outof in outofs:
        # gf does not like spaces and parens in asst names
        asst = asst.replace('(', '_').replace(')', '_').replace(' ', '_')
        header = header + \
            '{} / {}\n'.format(asst, int(outof))
    return header


def _make_gf_student_line(student, utorid=False, grades=None, outofs=None, comment=None):
    '''outofs is a List[(asst, grade)], as it must be ordered for gf.
    grades is a Grades object
    utorid: should we include a line for utorid?
    Either both grades and outofs are None (no grades) or both are not None (grades recorded).
    If comment is present, write a second line, too: with the comment.
    '''

    line = '{}    {} {}{}'.format(
        student.student_number,
        student.last if student.last else '',
        student.first if student.first else '',
        ',{}'.format(student.utorid) if utorid else '')

    if grades:
        line = (line + ',' +
                ','.join([str(round(grades.get_grade(asst), 1)) for (asst, grade) in outofs]) +
                '\n')

    if comment:
        line += '{}* {}\n'.format(student.student_number, comment)

    return line
'''Defauls values for various utils.'''

MAX_UTORID_LENGTH = 8

STUDENT_NUMBER_LENGTH = 10

# str methods of Student and Students will use this as default format/ordering
# if any of these are not present, they are omitted from the str
DEFAULT_STUDENT_STR = ('last', 'first', 'student_number', 'utorid',
                       'gitid', 'email', 'lecture', 'tutorial', 'id1', 'id2')

# TODO Fix this
DEFAULT_FORMULA_OUTOF = 100


def default_student_sort(student):
    '''Sort Student's by last name, then first name.'''

    return student.last + student.first

'''Defauls values for various utils.'''

MAX_UTORID_LENGTH = 8

STUDENT_NUMBER_LENGTH = 10

# str methods of Student and Students will use this as default format/ordering
# if any of these are not present, they are omitted from the str
DEFAULT_STUDENT_STR = ('last', 'first', 'student_number', 'utorid',
                       'gitid', 'email', 'lecture', 'tutorial', 'id1', 'id2')


def default_student_sort(student):
    '''Sort Student's by last name, then first name.'''

    return student.last + student.first


# TODO Fix this
DEFAULT_FORMULA_OUTOF = 100

RESERVED_QUERCUS_COLUMNS = (
    'Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Integration ID', 'Section',
    'Assignments Current Points',
    'Assignments Final Points',
    'Assignments Current Score',
    'Assignments Unposted Current Score',
    'Assignments Final Score',
    'Assignments Unposted Final Score',
    'Deliverables Current Points',
    'Deliverables Final Points',
    'Deliverables Current Score',
    'Deliverables Unposted Current Score',
    'Deliverables Final Score',
    'Deliverables Unposted Final Score',
    'Current Points', 'Final Points',
    'Current Score', 'Unposted Current Score',
    'Final Score', 'Unposted Final Score')

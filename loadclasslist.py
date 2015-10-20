"""Get a map of Students: by utsc id or by student number."""

class Student(object):
    """A Student has a utsc id (str), student number (str), last name
    (str), first name(s) (str), and email (str)."""
    
    def __init__(self, fields):
        self.utsc_id = fields[0]
        self.st_num = fields[1]
        self.lastname = fields[2]
        self.firstnames = fields[3]
        #self.email = self.utsc_id + '@utsc.toronto.edu'

def load_by_st_num(filename):
    """Create from the input class list 'filename' and return a
    dictionary of Students by student number."""

    return load(filename, 1)
	
def load_by_utsc_id(filename):
    """Create from the input class list 'filename' and return a
    dictionary of Students by student number."""

    return load(filename, 0)

def load(filename, field_num):
   
    d = {}
    for line in open(filename):
        fields = line.strip().split(',')
        d[fields[field_num]] = Student(fields)
    return d

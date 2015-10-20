import csv

def make_students_from_intranet(intranet_file):
    """Return dict of stunum->Student from the given Intranet classlist."""

    reader = csv.reader(open(intranet_file))
    reader.next() # skip header
    students = {}
    for row in reader:
        [stunum, email, lec, tut] = [row[0],row[-1],row[3],row[5]]
        [last, first] = row[1].split(',')
        students[stunum] = Student(None, stunum, last, first, email, lec, tut)
    return students

def update_utorids(students, bbfile):
    """Given a dictionary of stunum->Student and a Blackboard file,
    update the UTORIDs of Students, and return the resulting
    dictionary."""

    reader = csv.reader(open(bbfile))
    for row in reader:
        if row[3] not in students:
            print("Warning: %s not in students." % (row[3]))
            continue
        students[row[3]].set_utorid(row[0])

def print_catme_file(students):
    print("First, Last, Email, ID, Section")
    for student in students.values():
        print("%s,%s,%s,%s,%s" % (student.first[:20], student.last[:20], 
                                  student.email, student.utorid, student.tut))


class Student:
    def __init__(self, utorid, stunum, last, first, email=None, lec=None, tut=None):
        self.utorid = utorid
        self.stunum = stunum
        self.last = last
        self.first = first
        self.email = email
        self.lec = lec
        self.tut = tut

    def set_utorid(self, utorid):
        self.utorid = utorid

if __name__ == '__main__':
    students = make_students_from_intranet('intranetOct23.csv')
    update_utorids(students, 'bbOct23.csv')
    print_catme_file(students)


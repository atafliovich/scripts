def make_students_by(classlist, by_stnum=False):

    students = {}
    for line in classlist:
        tokens = line.strip().split(',')
        utorid = tokens[0]
        stnum = tokens[3]
        last = tokens[2]
        first = tokens[1]
        if by_stnum:
            students[stnum] = [utorid, last, first]
        else:
            students[utorid] = [stnum, last, first]
    return students

def make_grades_from_markus(csvfile, students):
    grades = {}
    for line in csvfile:
        tokens = line.strip().split(',')
        utorid = tokens[0]    # hard-code: MarkUs format
        grade = tokens[1]
        if grade == '""':
            grade = 0
        else:
            grade = round(float(grade))
        grades[utorid] = [str(grade)]
    return grades


def make_grades(csvfile, students):

    grades = {}
    for line in csvfile:
        tokens = line.strip().split(',')
        stnum = tokens[1]    # hard-code: Ainsley's csv file
        lab_grade = tokens[10]
        mid_grade = tokens[12]
        grades[stnum] = [lab_grade, mid_grade]
    return grades

def print_grades(grades, students):
    for (stnum, student) in students.items():
        utorid = student[0]
        last = student[1]
        first = student[2]
        st_grades = grades[utorid]
        print("%s    %s  %s\t%s" % (stnum, last, first, utorid), end='')
        print("\t" + "\t".join(st_grades))
        
def print_empty(students):

    for (stnum, student) in students.items():
        utorid = student[0]
        last = student[1]
        first = student[2]
        print("%s    %s  %s\t%s" % (stnum, last, first, utorid))
        
if __name__ == '__main__':

    import sys
    if len(sys.argv) != 3:
        print("Usage: makegrades.py csv-file classlist.grades")
        exit(1)

    csvfile = open(sys.argv[1])
    classlist = open(sys.argv[2])

    students = make_students_by(classlist, True)
    #students = make_students_by(classlist)
    grades = make_grades_from_markus(csvfile, students)
    print_grades(grades, students)
    #print_empty(students)

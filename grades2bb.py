'''Get the final grades from the CDF grades file (with no header or
comments) and fill in the Blackboard [curse] file.'''

from xlrd import open_workbook,XL_CELL_TEXT
from xlwt import Workbook
from xlwt import easyxf
from xlutils.copy import copy
import sys

ST_NUM_COL = 3 # column where student number appears

def read_grades(grades_file):
    '''Return a dictionary mapping student numbers to grades. Assumes
    grades_file is a CDF grades file with no comments.'''

    grades= {}
    all_lines = open(grades_file).readlines()
    for line in all_lines[all_lines.index('\n') + 1:]:
        line = line[:-1]  # strip newline character
        st_num, rest = line[:10], line[14:] # student number is first 10 chars
        last_name = rest[:rest.find('  ')]  # last name is between '    ' and '  '
        rest = rest[rest.find('  ') + 2:]
        tokens = rest.split('\t')

        if st_num[0] == '0':       # strip leading 0 in student number
            st_num = st_num[1:]   # because it doesn't appear on BB [curse]

        grade = tokens[IN_GRADE_COL - 2]
        if grade == '':    # empty in grades file means grade 0
            grade = '0'

        grades[st_num] = grade
    return grades


def fill_grades(grades, in_xl_file, out_xl_file):
    """Create a copy of the xls file 'in_xl_file' and call it
    'out_xl_file'. Fill in the OUT_GRADE_COL column in 'out_xl_file'
    from the dictionary 'grades'."""
    
    read_book = open_workbook(in_xl_file, formatting_info=True)
    read_sheet = read_book.sheet_by_index(0)
    write_book = copy(read_book)
    write_sheet = write_book.get_sheet(0)

    for row in range(1, read_sheet.nrows):
        st_num = read_sheet.cell_value(row, ST_NUM_COL)
        try:
            write_sheet.write(row, OUT_GRADE_COL, float(grades[str(int(st_num))]))
        except KeyError:
            print('Warning: no grade for', str(st_num))
        except ValueError:
            write_sheet.write(row, OUT_GRADE_COL, grades[str(int(st_num))])
    write_book.save(out_xl_file)


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print("Usage: python grades2bb.py <grades-file> <input-excel-file>" +
              " <output-excel-filename> <in-grade-col> <out-grade-col>")
        exit(1)
    IN_GRADE_COL = int(sys.argv[4])
    OUT_GRADE_COL = int(sys.argv[5])
    
    fill_grades(read_grades(sys.argv[1]), sys.argv[2], sys.argv[3])

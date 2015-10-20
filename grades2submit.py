"""Get the final grades from the CDF grades file and fill in the Excel
spreadsheet for submitting to the registrar. Assumes the last mark in
the CDF grades file is the final grade. Takes three file names as input:

python grades2submit.py <grades-file> <input-xls-file> <output-xls-file>

<grades-file> (the CDF grades file) and <input-xls-file> (the Excel
spreadsheet the Regisrtar wants) must exist.
<output-xls-file> will be created.
"""

from xlrd import open_workbook,XL_CELL_TEXT
from xlwt import Workbook
from xlwt import easyxf
from xlutils.copy import copy
import sys

ST_NUM_COL = 8 # column number in the Excel spreadsheet where student
               # number appears
FINAL_GRADE_COL = 12 # column number in the Excel spreadsheet where
               # the final grade appears

def read_grades(grades_file):
    '''Return the dictionary mapping student numbers to final
    grades.
    Parameters: grades_file : string, name/path of CDF grades file.
    Assumes the last mark in the file is the final grade.'''

    grades= {}
    all_lines = open(grades_file).readlines()
    for line in all_lines[all_lines.index('\n') + 1:]: # skip header
        tokens = line.rstrip().split()
        st_num, grade = tokens[0], tokens[-1]
        if len(st_num) == 10 and st_num[9] == '*': # skip comments
            continue
        grades[st_num] = grade
    return grades

def fill_grades(grades, in_xl_file, out_xl_file):
    """Create a copy of the xls file 'in_xl_file' and call it
    'out_xl_file'. Fill in the final grades column in 'out_xl_file'
    from the dictionary 'grades'."""
    
    read_book = open_workbook(in_xl_file, formatting_info=True)
    read_sheet = read_book.sheet_by_index(0)
    write_book = copy(read_book)
    write_sheet = write_book.get_sheet(0)

    for row in range(1, read_sheet.nrows):
        st_num = read_sheet.cell_value(row, ST_NUM_COL)
        try:
            write_sheet.write(row, FINAL_GRADE_COL, int(grades[str(int(st_num))]))
        except KeyError:
            print 'Warning: no grade for ' + str(st_num)
        except ValueError:
            write_sheet.write(row, FINAL_GRADE_COL, grades[str(int(st_num))])
    write_book.save(out_xl_file)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: python grades2submit.py <grades-file> <input-excel-file>" +
              " <output-excel-filename>")
        exit(1)

    fill_grades(read_grades(sys.argv[1]), sys.argv[2], sys.argv[3])

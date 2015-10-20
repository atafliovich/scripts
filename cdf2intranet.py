"""Take a CDF grades file and produce an Intranet grades file. Takes
file name as input. Prints to stdout. The second line of the Intranet
file will need to be filled in manually."""

import sys

def make_header(lines):
    """Print to stdout in incomplete header of the Intranet file that
    corresponds to the CDF grades file.

    Parameters: lines: list of strs, the lines of the CDF grades file.
    """

    grades = []
    for line in lines[:lines.index('\n')]: # the header lines
        if line.lstrip().startswith('*'): # skip comments
            continue
        [grade, sep, out_of] = line.partition(' / ')
        if sep:
            grades.append(grade)
        [grade, sep, rest] = line.partition(' = ')
        if sep:
            grades.append(grade)

    print ('"Student Number","Family Name","Given Names",' + 
           ','.join(grades))
    print ('"Weights (% of total mark)","",""' +
           ',' * len(grades))

def make_grades(lines):
    """Print to stdout the portion of hte Inrtanet file that follows
    the header (i.e. starting with line 3.

    Parameters: lines: list of strs, the lines of the CDF grades file.
    """

    for line in lines[lines.index('\n') + 1:]: # skip header 
        if line[10:14] != '    ': # skip comments, dropped and excluded
            continue
        st_num, sep, rest = line.rstrip().partition('    ')
        #if len(st_num) < 10: # pad student numbers
        #    st_num = '0' + st_num
        last_name, sep, rest = rest.partition('  ')
        rest = rest.split('\t')
        first_names = rest[0].strip()
        grades = rest[1:]

        print ','.join([st_num, last_name, first_names] +
                       grades)
        
def convert(cdf):
    """Print to stdout the Intranet file that corresponds to the
    CDF grades file in the file intranet.
    Parameters:
      cdf : string, name of file
    """
    
    lines = open(cdf).readlines()
    make_header(lines)
    make_grades(lines)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python cdf2intranet.py <cdf-file>")
        exit(1)

    convert(sys.argv[1])

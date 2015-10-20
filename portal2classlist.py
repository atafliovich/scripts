"""Takes a grades file from the portal. Produces a classlist I use for
my own purposes. Takes a filename. Writes output to stdout.
Output format is:

UTOR_ID,student-number,last-name,first-name0 first-name1 ...
"""

import sys

def portal_to_classlist(in_file):
    """Takes a valid file object. Writes to stdout."""

    in_file.readline() #skip the header
    
    for line in in_file:
        tokens = line.strip().split(',')
        
        utorid = tokens[2][1:-1] # get rid of quotes
        student_num = tokens[3][1:-1]
        first_names = tokens[1][1:-1]
        last_name = tokens[0][1:-1]
        print(','.join([utorid, student_num, last_name, first_names]))

def main():
    """Try to open input file. Process."""

    if len(sys.argv) != 2:
        print("Usage: python portal2classlist.py <portal-gradesfile>")
        exit(1)

    portal_to_classlist(open(sys.argv[1]))

if __name__ == '__main__':

    main()
        

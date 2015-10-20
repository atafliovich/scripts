'''Convert a classlist downloaded from Blackboard in the following format
UTORID,Last name, First names, student number, email
into a CDF grades file. Takes filename as input. Prints to stdout.
'''
import sys

def make_header(lines):
    """Print out the header of the CDF grades file.
    Parameters: lines : list of strs; two header lines of the Intranet
    file."""
    
    names = lines[0].rstrip().split(',')[3:]
    weights = lines[1].rstrip().split(',')[3:]

    for name in names:
        print name + ' / '

    print ALL + ' =',
    for (name, weight) in zip(names, weights):
        print name + ' : ' + weight,

    print

def make_grades(lines):
    """Print out the grades lines of the CDF grades file.
    Parameters: lines : list of strs; the grades lines of
    the Intranet file."""
    
    for line in lines:
        tokens = line.rstrip().split(',')
        st_num = tokens[0]
        last_name = tokens[1]
        first_names = tokens[2]
        grades = tokens[3:]

        print (st_num + '    ' +
               last_name + '  ' +
               first_names + '\t' +
               '\t'.join(grades))

def convert(intranet):
    """Print out the CDF grades file that corresponds to intranet.
    Parameters: intranet : str; name/path of the Intranet file.
    """
    
    # the first two lines make a header
    all_lines = open(intranet).readlines()
    make_header(all_lines[:2])
    print
    make_grades(all_lines[2:])

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python intranet2cdf.py <intranet-file>")
        exit(1)

    convert(sys.argv[1])

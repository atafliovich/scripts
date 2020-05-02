#!/usr/bin/python3

'''
Read a Blackboard file in format
    utorid, firstnames, lastname, studentnumber, anything else ...
and print to stdout the corresponding lines of a gf file.
'''

import sys
import csv

if len(sys.argv) != 2:
    print('Usage: bb2grade classlist.csv [ > stdoutfile]', file=sys.stdout)
    sys.exit(1)

for line in csv.reader(open(sys.argv[1], 'U')):
    utorid, first, last, stunum = line[:4]
    print('%s    %s %s,%s' % (stunum.zfill(10), first, last, utorid))

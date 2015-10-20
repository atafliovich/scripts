#!/usr/bin/python2

# CAUTION! Requires Python 2.

# Modified by A. Tafliovich to generate 10-digit student numbers.

# Read a Blackboard grade-centre file (saved as "Comma Separated Values") and
# write to standard output lines that would be the corresponding student
# records in a DCS grade file. The input file name is the single command-line
# argument:
#
#   bb2grade gradecentrefile.csv
#
# The input lines in the grade centre file are assumed to contain these
# fields, separated by tabs: family name, given names, UTORid, student number,
# others. We don't need the others, so we just keep the UTORid as a "mark".
#
# The first line is assumed to contain column titles, so if it doesn't contain
# a valid student number it's just ignored. Otherwise, bad student numbers
# cause an error message (for some really simple-minded definition of "bad").

# Jim Clarke, Feb 2011

import sys, csv

if len(sys.argv) != 2:
    print >> sys.stderr, 'Usage: bb2grade bbgrades.csv [ > stdoutfile]'
    sys.exit(1)

reader = csv.reader(open(sys.argv[1], 'U')) # 'U' is universal-newline mode

lineNum = 0
for line in reader:
    lineNum += 1
    #utorid, family, given, stunum = line[:4]
    utorid, given, family, stunum = line[:4]
    if not stunum[0].isdigit():
        if lineNum == 1:
            continue
        else:
            print >> sys.stderr, 'Line ', lineNum, ' has bad student number:'
            print >> sys.stderr, line
            sys.exit(1)
            
    stunum = '0' * (10 - len(stunum)) + stunum
    output_line = stunum + '    ' + family + '  ' + given + '\t' + utorid
    print output_line

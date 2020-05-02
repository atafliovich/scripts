#!/usr/bin/python3

GF_FILE = 'all.gf'
MARKUS_FILE = 'markus.csv'

with open(GF_FILE) as grades:
    grades_lines = [line.strip().split(',') for line in grades.readlines()[12:] if '*' not in line]
    markus_lines = [','.join(line[1:-2] + [line[-1]]) for line in grades_lines]

with open(MARKUS_FILE, 'w') as markus:
    markus.write('\n'.join(markus_lines))

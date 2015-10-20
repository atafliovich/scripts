"""Takes a classlist with no emails and a file with student emails
(sent by John Harper) and produces a full classlist or an email list,
depending on the third argument ('full' or 'email').
Takes two filenames. Writes output to stdout.

Input format of classlist is:
UTOR_ID,student-number,last-name,first-name0 first-name1 ...

Input format of emaillist is:
0student-number email

Output format is:
UTOR_ID,student-number,last-name,first-name0 first-name1 ..., email

or

last-name,first-name0 first-name1 ..., email
"""

import sys

def get_emails(email_list):
    """Take a valid file object. Return a dict student_number -> email."""

    emails = {}
    for line in email_list:
        (stu_num, email) = line.strip().split()
        emails[stu_num] = email
    return emails

def add_emails(classlist, email_list, full):
    """Take two valid file objects. Write to stdout."""

    emails = get_emails(email_list)
    
    for line in classlist:
        (utorid, st_num, last_name, first_names)= line.strip().split(',')
        st_num = '0' + st_num
        if full:
            print(','.join([utorid, st_num, last_name, first_names, emails[st_num]]))
        else:
            print(','.join([last_name, first_names, emails[st_num]]))
            
def main():
    """Try to open input files. Process."""

    if len(sys.argv) != 4:
        print("Usage: python addemails.py <classlist> <emaillist> full/email")
        exit(1)

    add_emails(open(sys.argv[1]), open(sys.argv[2]), sys.argv[3] == 'full')
        
if __name__ == '__main__':

    main()
        

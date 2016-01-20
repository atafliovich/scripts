"""Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students.
"""

import argparse
import os
import sys
import time
from utils import Student
from utils import load_bb

subject = "CSC C24: grading results for Lab01"
bbfile = "/cmshome/tafliovi/c24/jan7.csv"
path_prefix = "/cmshome/tafliovi/c24/submissions"
path_suffix = "lab01/result.txt"

sender = "atafliovich@utsc.utoronto.ca"
sendmail_loc = "/usr/sbin/sendmail"

def send_mail(recipient, subject, message_body):
    """(str, str, str) -> NoneType
    
    Send an email to recepient with subject line subject
    and message body message_body.
    """
    
    # Build the message header
    header = ("From: %s\nTo: %s\nSubject: %s\r\n\r\n" %
              (sender, recipient, subject))

    # Actually send the message
    email = os.popen("%s -t" % (sendmail_loc), "w")
    email.write(header + message_body)
    email_status = email.close()


def send_mails(students, subject, path_pref, path_suff):
    """({str: Student}, str, str, str) -> NoneType
    
    Send an email to each student in the dictionary of Students (by
    student_id), with subject subject and the message body being the
    contents of a file path_pref/Student.utorid/path_suff.
    """

    for student in students.values():
        try:
            markfile = open(os.path.join(path_pref,
                                         student.student_id,
                                         path_suff))
            body = markfile.read()
            markfile.close()

            send_mail(student.email, subject, body)
        except IOError as error:
            print("No result for %s: %s" % (student.student_id, error))


if __name__ == "__main__":

    # get args
    parser = argparse.ArgumentParser(
        description=('Email contents of result files to students.\n' +
                     'If an optional arg is not specified, the value defined at the top of this file is used.'))
    parser.add_argument('--subject',
                        help='The subject line.')
    parser.add_argument('--classlist',
                        help='Path to the classlist file in BB format.')
    parser.add_argument('--path_prefix',
                        help='Prefix of the path to the file to email: up to student submission directory.')
    parser.add_argument('--path_suffix',
                        help='Sufffix of the path to the file to email: from the student submission directory.')
    args = parser.parse_args()

    # email        
    students = load_bb(open(args.classlist), False) if args.classlist else load_bb(open(bbfile), False)
    send_mails(students, 
               subject, 
               args.path_prefix if args.path_prefix else path_prefix,
               path_suffix if args.path_suffix else path_suffix)

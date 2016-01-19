"""Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students.
"""

import argparse
import os
import sys
import time
from util import Student
from util import load_bb

course = "CSC C24"
asst = "Lab 1"
bbfile = "/cmshome/tafliovi/send/jan7.csv"
path_prefix = "/cmshome/tafliovi/send/lab01"
path_suffix = ""

sender = "atafliovich@utsc.toronto.edu"
sendmail_loc = "/usr/sbin/sendmail"
subject = "%s: grading results for %s" % (course, asst)


def send_mail(recipient, subject, message_body):
    """(str, str, str) -> NoneType
    
    Send an email to recepien with subject line subject
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
    
    Send an email to each student in the dictionary of Students (by student_id),
    with subject subject and the message body being the contents of a file
    path_pref/Student.utorid/path_suff.
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
            print("No result for %s: %s" % student.student_id, error)


if __name__ == "__main__":

    # get args
    parser = argparse.ArgumentParser(
        description=('Email contents of result files to students.'))
    parser.add_argument('classlist',
                        help='Path to the classlist file in BB format.')
    args = parser.parse_args()

    # email
    students = load_bb(args.classlist)
    send_mails(students, subject, path_prefix, path_suffix)

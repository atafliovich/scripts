"""Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students.
"""
# TODO: this needs updating to work with new utils

import argparse
import os
from utils import load_bb

SUBJECT = "CSC C24: grading results for lab09"
CLASSLIST = "/cmshome/tafliovi/c24/feb24.csv"
PATH_PREFIX = "/cmshome/tafliovi/c24/submissionsLab9"
PATH_SUFFIX = "lab09/result.txt"

SENDER = "atafliovich@utsc.utoronto.ca"
SENDMAIL_LOC = "/usr/sbin/sendmail"


def send_mail(recipient, subject, message_body):
    """Send an email to recepient with subject line subject and message
    body message_body.

    """

    # Build the message header
    header = ("From: %s\nTo: %s\nSubject: %s\r\n\r\n" %
              (SENDER, recipient, subject))

    # Actually send the message
    email = os.popen("%s -t" % (SENDMAIL_LOC), "w")
    email.write(header + message_body)
    email.close()


def send_mails(students, subject, path_pref, path_suff):
    """Send an email to each student in the dictionary of Students (by
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
    STUDENTS = load_bb(open(args.classlist), False) if args.classlist else load_bb(
        open(CLASSLIST), False)
    send_mails(STUDENTS,
               SUBJECT,
               args.path_prefix if args.path_prefix else PATH_PREFIX,
               PATH_SUFFIX if args.path_suffix else PATH_SUFFIX)

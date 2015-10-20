"""Email marks, rubrics, autotester results, etc. to
students. Basically, email text files to students."""

import os
import sys
import time
from loadclasslist import load_by_utsc_id

sender = "atafliovich@utsc.toronto.edu"
sendmail_loc = "/usr/sbin/sendmail"
path_prefix = "/users/h02/atafliovich/120/assts/a"

def send_mail(recipient, subject, message_body):
    """Send an email to 'recepient' (str) with subject 'subject' (str)
    and message body 'message_body' (str)."""
    
    # Build the message header
    header = ("From: %s\nTo: %s\nSubject: %s\r\n\r\n" %
              (sender, recipient, subject))

    # Actually send the message
    email = os.popen("%s -t" % (sendmail_loc), "w")
    email.write(header + message_body)
    email_status = email.close()

def send_mails(students, subject, path_pref, path_suff):
    """Send an email to each student in the dictionary of Students
    'students', with subject 'subject' and the message body from a
    file path_pref/login/path_suff."""

    for student in students.values():
        try:
            markfile = open(os.path.join(path_pref,
                                         student.utsc_id,
                                         path_suff))
            body = markfile.read()
            markfile.close()

            send_mail(student.email, subject, body)
        except:
            print "No result for %s." % student.utsc_id

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "python emailmarks.py <classlist> <assignment #>"
        sys.exit(0)

    students = load_by_utsc_id(sys.argv[1])
    asst_no = sys.argv[2]
    subject = "A20: Marked assignment %s" % asst_no
    path = os.path.join(path_prefix + asst_no, "marking", "marked")
    send_mails(students, subject, path, 
               os.path.join("a" + asst_no, "cover.txt"))

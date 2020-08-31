"""A new set of utilities to work with MarkUs, Quercus, Intranet, CDF
grades files, CATME files, and what not.
Work in progress.

"""

def make_team_to_students(students):
    '''Return a dict mapping team name to Student list.
    students is a Students object. Each Student must heave team attribute set.
    '''

    team_to_students = {}
    for student in students:
        assert student.team is not None
        members = team_to_students.get(student.team, [])
        members.append(student)
        team_to_students[student.team] = members
    return team_to_students


def make_team_to_emails(students):
    '''Return a dict mapping team name to list of emails of team members.

    students is a Students object. Each Student must heave team and
    email attributes set.

    '''

    team_to_emails = {}
    for student in students:
        assert student.team is not None and student.email is not None
        emails = team_to_emails.get(student.team, [])
        emails.append(student.email)
        team_to_emails[student.team] = emails
    return team_to_emails


def make_yaml_grading_sheet(students, team_to_ta_email):
    '''Return a List[dict] that can be dumped to YAML for Thierry's
    grading rubric on grademywork.

    students is a Students object.
    team_to_ta_email is a Dict[team_name: str, ta_email: str].

    '''

    team_to_emails = make_team_to_emails(students)

    to_yaml = []
    for team, emails in team_to_emails.items():
        sheet = team
        write = [team_to_ta_email[team]]
        audit = [ta_email for ta_email in set(team_to_ta_email.values())
                 if ta_email not in write]
        read = emails
        to_yaml.append({'sheet': sheet, 'write': write,
                        'audit': audit, 'read': read})
    return to_yaml

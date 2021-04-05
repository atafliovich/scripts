"""Utilities to work with grademywork."""

import requests


EMAIL = 'anya@cs.utoronto.ca'
PASSWORD = ''
OWNER = 'atafliovich'


API = 'https://grademy.work/api/'
# assessment
ASSESSMENT_FORMAT_STR = '{}users/{}/assessments/{{}}/'.format(API, OWNER)
# (assessment, sheet)
SHEET_FORMAT_STR = '{}sheets/{{}}/'.format(ASSESSMENT_FORMAT_STR)


def get_assessment(session, assessment_name):
    """Return a json assessment with assessment_name."""

    return session.get(ASSESSMENT_FORMAT_STR.format(assessment_name)).json()


def get_sheet(session, assessment_name, sheet_id):
    """Return a json sheet for assessment_name with sheetID sheet_id."""

    return session.get(SHEET_FORMAT_STR.format(assessment_name, sheet_id)).json()


def get_sheet_ids(user, assessment_name):
    """Return a list of sheetIDs in assessment_name."""

    return user['privileges']['{}/{}'.format(OWNER, assessment_name)]['sheets']


def get_grades(session, user, assessment_name):
    """Return a Dict[team_num, grade] for assessment_name."""

    assessment = get_assessment(session, assessment_name)
    points_questions = get_points_questions(assessment)
    sheets = (get_sheet(session, assessment_name, sheet_id)
              for sheet_id in get_sheet_ids(user, assessment_name))

    return {get_team(sheet): get_grade(sheet, points_questions)
            for sheet in sheets}


def get_team(sheet):
    """Return team_num for sheet."""

    return sheet['caption']


def get_grade(sheet, points_questions):
    """Return the total number of points in sheet.

    points_questions is a list of IDs of questions of type 'Points'.

    """

    return sum(float(answer['value'])
               for answer in sheet['answers']
               if answer['questionId'] in points_questions)


def get_points_questions(assessment):
    """Return a list of IDs of questions of type 'Points' from assessment."""

    return [question['id']
            for rubric in assessment['rubrics']
            for question in rubric['questions']
            if question['type'] == 'Points']


def start_session(email, password):
    """Return (session, user).
    """

    session = requests.Session()
    user = session.post('{}login'.format(API),
                        json=({'email': email,
                               'password': password})).json()
    return (session, user)


if __name__ == '__main__':

    SESSION, USER = start_session(EMAIL, PASSWORD)

'''
Full specs for Quiz:
 https://canvas.instructure.com/doc/api/quizzes.html
Full specs for QuizQuestion:
 https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create
'''

from canvasapi import Canvas

API_URL = "https://q.utoronto.ca"

# TODO: Go to https://q.utoronto.ca/profile/settings to generate an
# Access Token. Copy it immediately and paste here.
API_KEY = ""

CANVAS = Canvas(API_URL, API_KEY)

# TODO: This is the course ID. The easiest way to get it is to look
# the URL.  For example, my CSCC01 on Quercus is
# https://q.utoronto.ca/courses/158528 and so the ID of this course is
# "158528".
COURSE_ID = "158528"

COURSE = CANVAS.get_course(COURSE_ID)

SURVEY = {
    'title': 'Feedback for Instructor',
    'description': '''<p>This survey is <strong>anonymous</strong>. Please, take the time
to complete it and improve everyone's experience in the course!</p>''',
    'quiz_type': 'survey',
    # 'assignment_group_id': '',
    'hide_results': 'always',
    'allowed_attempts': 1,
    'due_at': '2020-07-15 23:59',
    'lock_at': '2020-07-15 23:59',
    'unlock_at': '2020-07-09 18:00',
    'anonymous_submissions': True,
    'published': False
}

Q1 = {
    'question_name': 'Pacing of Lectures',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>pacing of the lectures</strong> is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very slow', 'weight': 0.0},
                {'text': 'somewhat slow', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat fast', 'weight': 0.0},
                {'text': 'very fast', 'weight': 0.0}]
}

Q2 = {
    'question_name': 'Difficulty of Lectures',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>difficulty of the lecture material</strong> is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very easy', 'weight': 0.0},
                {'text': 'somewhat easy', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat hard', 'weight': 0.0},
                {'text': 'very hard', 'weight': 0.0}]
}

Q3 = {
    'question_name': 'Pacing of Tutorials',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>pacing of the tutorials</strong> is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very slow', 'weight': 0.0},
                {'text': 'somewhat slow', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat fast', 'weight': 0.0},
                {'text': 'very fast', 'weight': 0.0}]
}

Q4 = {
    'question_name': 'Difficulty of Tutorials',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>difficulty of the tutorial material</strong> is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very easy', 'weight': 0.0},
                {'text': 'somewhat easy', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat hard', 'weight': 0.0},
                {'text': 'very hard', 'weight': 0.0}]
}

Q5 = {
    'question_name': 'Delivery',
    'question_type': 'multiple_choice_question',
    'question_text': '''<p>This question is about the <strong>method of delivery</strong>
of lecture and tutorial materials. So far we had live online lectures
and tutorials, posted reading materials, posted videos, piazza
discussion board, and live online office hours. </p> <p>The methods of
delivering lectures so far (as best as can be done under the
circumstances!) are: </p>''',
    'points_possible': 0.0,
    'answers': [{'text': 'completely inadequate, need a new method (see my comments below)',
                 'weight': 0.0},
                {'text': 'could be better, need some modifications (see my comments below)',
                 'weight': 0.0},
                {'text': 'all good, cannot think of any suggestions',
                 'weight': 0.0}]
}

Q6 = {
    'question_name': 'Workload of Project',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>amount of work required</strong> on the project is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very light', 'weight': 0.0},
                {'text': 'somewhat light', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat heavy', 'weight': 0.0},
                {'text': 'very heavy', 'weight': 0.0}]
}

Q7 = {
    'question_name': 'Difficulty of Project',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>level of difficulty</strong> of the project is:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very easy', 'weight': 0.0},
                {'text': 'somewhat easy', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat hard', 'weight': 0.0},
                {'text': 'very hard', 'weight': 0.0}]
}

Q8 = {
    'question_name': 'Difficulty of Midterm',
    'question_type': 'multiple_choice_question',
    'question_text': '<p>The <strong>level of difficulty</strong> of the midterm was:</p>',
    'points_possible': 0,
    'answers': [{'text': 'very easy', 'weight': 0.0},
                {'text': 'somewhat easy', 'weight': 0.0},
                {'text': 'just right', 'weight': 0.0},
                {'text': 'somewhat hard', 'weight': 0.0},
                {'text': 'very hard', 'weight': 0.0}]
}

Q9 = {
    'question_name': 'Available help',
    'question_type': 'multiple_choice_question',
    'question_text': '''<p>The <strong>opportunities to get help</strong> from instructor
and TAs are:</p>''',
    'points_possible': 0,
    'answers': [{'text': 'completely inadequate, need a new method (see my comments below)',
                 'weight': 0.0},
                {'text': 'could be better, need some modifications (see my comments below)',
                 'weight': 0.0},
                {'text': 'all good, cannot think of any suggestions',
                 'weight': 0.0}]
}

Q10 = {
    'question_name': 'Stress / COVID19',
    'question_type': 'multiple_choice_question',
    'question_text': '''<p>To what extent to you agree with the following statement?</p>
    <p>I find that COVID19 is negatively affecting my ability to study
    because of increased stress levels, home situation, remote nature of the course, etc.</p>''',
    'points_possible': 0,
    'answers': [{'text': 'strongly disagree', 'weight': 0.0},
                {'text': 'disagree', 'weight': 0.0},
                {'text': 'agree', 'weight': 0.0},
                {'text': 'strongly agree', 'weight': 0.0}]
}


Q11 = {
    'question_name': 'Suggestions',
    'question_type': 'essay_question',
    'question_text': '''<p> Please, type your <strong>comments</strong> and
<strong>suggestions for improvements</strong> here: </p>''',
    'points_possible': 0,
    'answers': []
}


def create(quiz_specs, questions):
    '''Create the quiz!'''

    quiz = COURSE.create_quiz(quiz_specs)

    for question in questions:
        quiz.create_question(question=question)

    return quiz


if __name__ == '__main__':

    import sys

    QUESTIONS = [getattr(sys.modules[__name__], 'Q{}'.format(i))
                 for i in range(1, 12)]

    create(SURVEY, QUESTIONS)

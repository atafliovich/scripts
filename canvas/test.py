'''
Full specs for Quiz:
 https://canvas.instructure.com/doc/api/quizzes.html
Full specs for QuizQuestion:
 https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create
'''

from canvasapi import Canvas
from .generic import INTEGRITY_1, INTEGRITY_2

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

# Can use HTML in all text fields.
QUIZ_SETTINGS = {  # To understand what these are, mostly, take a look at the
    # options on an "Edit Quiz" page on quercus.
    'title': 'Test Quiz',
    'description': '''<p>This is a sample quiz uploaded to quercus using the API.</p>
    <p>You will be presented with one question at a time. Once you
    submit an answer to a question, you <strong>cannot go
    back</strong> to it.</p>''',
    'quiz_type': 'assignment',  # 'practice_quiz', 'assignment', 'graded_survey', 'survey'
    # 'assignment_group_id': '',
    'time_limit': '180',   # in minutes
    'shuffle_answers': True,
    'hide_results': 'always',  # 'until_after_last_attempt'
    'show_correct_answers': False,
    # 'show_correct_answers_at': '',  # timestamp
    # 'hide_correct_answers_at': '',
    # 'allowed_attempts': '',
    # 'scoring_policy': '',  # 'keep_highest' or 'keep_latest' (only for multiple attempts)
    'one_question_at_a_time': True,
    'cant_go_back': True,
    # 'access_code': '',
    # 'ip_filter': '',
    'due_at': '2020-07-07 17:00',
    'lock_at': '2020-07-07 17:00',
    'unlock_at': '2020-07-07 14:00',
    # Highly recommended to "publish" manually online once the quiz is fully set up
    'published': False,
    # 'one_time_results': '',
    # 'only_visible_to_overrides': ''
}

######### QUESTIONS ##########

Q0 = {
    'question_name': 'Test True/False Question',
    'question_type': 'true_false_question',
    'question_text': 'true or false?',
    'points_possible': 16,
    'position': 1,
    'correct_comments': 'Correct answer!',
    'incorrect_comments': 'Sorry, incorrect.',
    'answers': [
        {'answer_text': 'True', 'weight': 0},
        {'answer_text': 'False', 'weight': 100},
    ]
}

Q1 = {
    'question_name': 'Test MC Question',
    'question_type': 'multiple_choice_question',
    'question_text': 'One, two, or three?',
    'points_possible': 5,
    'position': 2,
    'answers': [
        {'answer_text': 'one', 'weight': 0},
        {'answer_text': 'two', 'weight': 100},
        {'answer_text': 'three', 'weight': 0},
        {'answer_text': 'dunno', 'weight': 100}
    ]
}


Q2 = {
    'question_name': 'Test Multiple Dropdown Question',
    'question_type': 'multiple_dropdowns_question',
    'question_text': 'Here is the [Option1] and here is the [Option2] and done.',
    'points_possible': 6,
    'position': 3,
    'answers': [
        {'answer_text': 'Nope11', 'blank_id': 'Option1', 'answer_weight': 0},
        {'answer_text': 'Nope12', 'blank_id': 'Option1', 'answer_weight': 0},
        {'answer_text': 'Yep1', 'blank_id': 'Option1', 'answer_weight': 100},
        {'answer_text': 'Nope21', 'blank_id': 'Option2', 'answer_weight': 0},
        {'answer_text': 'Nope22', 'blank_id': 'Option2', 'answer_weight': 0},
        {'answer_text': 'Yep2', 'blank_id': 'Option2', 'answer_weight': 100}
    ]
}

Q3 = {
    'question_name': 'Test Short Answer Question',
    'question_type': 'short_answer_question',
    'question_text': 'Your short answer, please.',
    'points_possible': 2,
    'position': 4,
    'answers': [
        {'answer_text': 'yay1', 'answer_weight': 100},
        {'answer_text': 'yay2', 'answer_weight': 100}
    ]
}

# distractors
WRONG = '''no
not
non'''

Q4 = {
    'question_name': 'Test Matching Question',
    'question_type': 'matching_question',
    'question_text': 'Matching left to right and right to left',
    'points_possible': 10,
    'position': 5,
    'answers': [
        {'answer_match_left': 'left1', 'answer_match_right': 'right1'},
        {'answer_match_left': 'left2', 'answer_match_right': 'right2'},
        {'answer_match_left': 'left3', 'answer_match_right': 'right3'},
        # can't get distractors to work :(
        {'matching_answer_incorrect_matches': WRONG}
    ]
}

Q5 = {
    'question_name': 'Test Multiple Answers Question',
    'question_type': 'multiple_answers_question',
    'question_text': 'There are multiple answers here',
    'points_possible': 5,
    'position': 6,
    'answers': [
        {'answer_text': 'nope1', 'weight': 0},
        {'answer_text': 'yep1', 'weight': 100},
        {'answer_text': 'yep2', 'weight': 100},
        {'answer_text': 'nope3', 'weight': 0}
    ]
}

Q6 = {
    'question_name': 'Test File Upload Question',
    'question_type': 'file_upload_question',
    'question_text': 'Here we upload a file',
    'points_possible': 5,
    'position': 7
}

Q7 = {
    'question_name': 'Test Fill In Multiple Blanks Question',
    'question_type': 'fill_in_multiple_blanks_question',
    'question_text': 'Fill in [Blank1] here and [Blank2] there.',
    'points_possible': 10,
    'position': 8,
    'answers': [
        {'answer_text': 'yay11', 'blank_id': 'Blank1', 'answer_weight': 100},
        {'answer_text': 'yay12', 'blank_id': 'Blank1', 'answer_weight': 100},
        {'answer_text': 'yay21', 'blank_id': 'Blank2', 'answer_weight': 100},
        {'answer_text': 'yay22', 'blank_id': 'Blank2', 'answer_weight': 100},
        {'answer_text': 'yay23', 'blank_id': 'Blank2', 'answer_weight': 100},
    ]
}

Q8 = {
    'question_name': 'Test Numerical Question: exact',
    'question_type': 'numerical_question',
    'question_text': 'What is the exact number? yet within margin of error... ',
    'points_possible': 10,
    'position': 9,
    'answers': [
        {"numerical_answer_type": "exact_answer",
         'answer_text': '', "exact": 42, 'margin': 2, 'answer_weight': 100},
    ]
}

Q9 = {
    'question_name': 'Test Numerical Question: precision',
    'question_type': 'numerical_question',
    'question_text': 'What is the answer (precision)',
    'points_possible': 10,
    'position': 10,
    'answers': [
        {"numerical_answer_type": "precision", "approximate": 4200.0,
         "precision": 2, 'answer_weight': 100},
    ]
}

Q10 = {
    'question_name': 'Test Numerical Question: range',
    'question_type': 'numerical_question',
    'question_text': 'What is the answer (range)',
    'points_possible': 10,
    'position': 11,
    'answers': [
        {"numerical_answer_type": "range_answer",
         "from": 1, "to": 4, 'answer_weight': 100},
    ]
}

Q11 = {
    'question_name': 'Test Essay Question',
    'question_type': 'essay_question',
    'question_text': 'Free form answer / essay',
    'points_possible': 2,
    'position': 12
}


if __name__ == '__main__':

    import sys

    QUIZ = COURSE.create_quiz(QUIZ_SETTINGS)

    # Q1, Q2, ..., Q11
    QNS = [getattr(sys.modules[__name__], 'Q{}'.format(i)) for i in range(12)]

    QUIZ.create_question(question=INTEGRITY_1)
    QUESTIONS = [QUIZ.create_question(question=QN) for QN in QNS]
    QUIZ.create_question(question=INTEGRITY_2)

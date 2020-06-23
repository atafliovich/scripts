'''
Full API for Quiz:
 https://canvas.instructure.com/doc/api/quizzes.html
Full API for QuizQuestion:
 https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create
'''

from canvasapi import Canvas
from canvasutils import generate_answers, value_of

API_URL = "https://q.utoronto.ca"
API_KEY = "11834~SUp5EUiSGkgEtdEPHrDcWsv9UBhxmP6hVp5k2TXa36RqzY9dv4EwN7Go8VT0FHSo"
C01 = "158528"

canvas = Canvas(API_URL, API_KEY)
c01 = canvas.get_course(C01)

# Can use HTML in all text fields.
QUIZ = {
    'title': 'Test quiz',
    'description': 'Test description',
    'quiz_type': 'assignment',
    # 'assignment_group_id': '',
    'time_limit': '42',   # in minutes
    # 'shuffle_answers': True/Fale,
    'hide_results': 'always',
    'show_correct_answers': False,
    # 'show_correct_answers_at': '',
    # 'hide_correct_answers_at': '',
    # 'allowed_attempts': '',
    # 'scoring_policy': '',
    # 'one_question_at_a_time': '',
    # 'cant_go_back': '',
    # 'access_code': '',
    # 'ip_filter': '',
    'due_at': '2020-06-22 16:00',
    'lock_at': '2020-06-22 16:30',
    'unlock_at': '2020-06-21 17:00',
    # 'published': False,
    # 'one_time_results': '',
    # 'only_visible_to_overrides': ''
}

# QUESTIONS

Q0 = {
    'question_name': 'Test True/False 0',
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
    'question_name': 'Test MC 1',
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
    'question_name': 'Test Multiple Dropdown 2',
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
    'question_name': 'Test Short Answer Question 3',
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
    'question_name': 'Test Matching Question 4',
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
    'question_name': 'Test Multiple Answers 5',
    'question_type': 'multiple_answers_question',
    'question_text': 'There are multiple answers here',
    'points_possible': 5,
    'position': 6,
    'answers': [
        {'answer_text': 'nope1', 'weight': 0},
        # weight can assign partial marks? Doesn't look like it. Just 0 or non-0.
        {'answer_text': 'yep1', 'weight': 100},
        {'answer_text': 'yep2', 'weight': 100},
        {'answer_text': 'nope3', 'weight': 0}
    ]
}

Q6 = {
    'question_name': 'Test File Upload 6',
    'question_type': 'file_upload_question',
    'question_text': 'Here we upload a file',
    'points_possible': 5,
    'position': 7
}

Q7 = {
    'question_name': 'Test Fill In Multiple Blanks 7',
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
    'question_name': 'Test Numerical Question: exact 8',
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
    'question_name': 'Test Numerical Question: precision 9',
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
    'question_name': 'Test Numerical Question: range 10',
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
    'question_name': 'Test Essay Question 11',
    'question_type': 'essay_question',
    'question_text': 'Free form answer / essay',
    'points_possible': 2,
    'position': 12
}

# Now this one can be pretty interesting!
# Worth looking at:
# https://community.canvaslms.com/groups/canvas-developers/blog/2019/05/11/using-python-to-create-calculated-questions

TEXT = '''Suppose we begin with:
<p>
>>> a = [x]
>>> b = [y]
>>> b = a
>>> a = [z]
>>> b = b + 1
</p>
What is the value of b?
'''

VARS = [{'name': 'x', 'min': 1.0, 'max': 10.0, 'scale': 0},
        {'name': 'y', 'min': 10.0, 'max': 20.0, 'scale': 0},
        {'name': 'z', 'min': 1.0, 'max': 20.0, 'scale': 0}]

ANS = generate_answers(VARS, lambda vs: value_of('x', vs) + 1, 5)

Q12 = {
    'question_name': 'Test Calculated Question 12',
    'question_type': 'calculated_question',
    'question_text': TEXT,
    'points_possible': 10,
    'position': 13,
    'formulas': ['b = x + 1'],
    'variables': VARS,
    'answers': ANS
}


if __name__ == '__main__':

    import sys

    # students = list(c01.get_users(enrollment_type=['student'], include=['email']))
    # TODO: write @static_method in Students load_from_quercus_API

    # assignment_group = c01.create_assignment_group(
    #    name='Test group', position=1, weight=0)

    # QUIZ.update({'assignment_group_id': assignment_group.id})
    # quiz = c01.create_quiz(QUIZ)

    quiz = c01.get_quizzes(search_term='Test quiz')[0]  # in general?

    QNS = [getattr(sys.modules[__name__], 'Q{}'.format(i)) for i in range(13)]

    #qns = [quiz.create_question(question=QN) for QN in QNS]

    # for q in quiz.get_questions():
    #    q.delete()

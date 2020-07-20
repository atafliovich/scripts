'''Some useful constants for Quercus Quizzes.'''

INTEGRITY_TEXT1 = '''<h1>Academic Integrity</h1> <p>I pledge to honour myself and my
community by assuring that the work I do on this exam fully represents
my own knowledge and ideas. I will feel proud of my work here when I
am done because I know that it was my own and only mine.</p>'''

INTEGRITY_TEXT2 = '''<h1>Academic Integrity</h1> <p>Congratulations — you've made it to
the end of the exam! We hope that you feel proud of the work that you
did here because you know that it was <b>your own and no one
else's</b>. Please know that all suspected cases of academic
dishonesty <b>will be investigated</b> following the procedures
outlined in the Code of Behaviour on Academic Matters. If you have
violated that Code, <b>admitting it now will significantly reduce</b>
any penalty you incur if it's discovered by your instructor
later. Admitting your mistakes is as much a matter of pride as never
making them from the beginning. Thus, please check the appropriate
statement below:</p>'''

INTEGRITY_OP1 = '''I confirm that the work I've done here is my own and no one else's,
in line with the principles of scholarship and the University of
Toronto's Code of Behaviour.'''

INTEGRITY_OP2 = '''I regret that I violated the Code of Behaviour on this exam and
would like to admit that now so that I can take responsibility for my
mistake.'''

INTEGRITY_1 = {
    'question_name': 'Academic Integrity 1',
    'question_type': 'true_false_question',
    'question_text': INTEGRITY_TEXT1,
    'points_possible': 0,
    'position': 1,  # looks like this will only work if all quiz
                    # questions specify position; otherwise, add
                    # first.
    'answers': [
        {'answer_text': 'True', 'weight': 100},
        {'answer_text': 'False', 'weight': 0},
    ]
}

INTEGRITY_2 = {
    'question_name': 'Academic Integrity 2',
    'question_type': 'true_false_question',
    'question_text': INTEGRITY_TEXT2,
    'points_possible': 0,
    'position': 1,  # looks like this will only work if all quiz
                    # questions specify position; otherwise, add
                    # last.
    'answers': [
        {'answer_text': INTEGRITY_OP1, 'weight': 100},
        {'answer_text': INTEGRITY_OP2, 'weight': 0},
    ]
}

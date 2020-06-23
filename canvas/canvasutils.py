import random


def generate_answer(variables, formula):
    '''Generate one answer to include in the canvas QuizQuestion.
    variables: [{'name': name, 'min': min, 'max': max, 'scale': scale}]
    formula: a function that takes variables and returns the correct numeric answer.
    '''

    answer_variables = [
        {'name': variable['name'],
         'value': random.randint(variable['min'], variable['max'])}
        for variable in variables]
    answer_value = formula(answer_variables)
    return {'weight': 100, 'variables': answer_variables, 'answer_text': answer_value}


def generate_answers(variables, formula, num):
    '''Generate num answers to include in the canvas QuizQuestion.
    variables: [{'name': name, 'min': min, 'max': max, 'scale': scale}]
    formula: a function that takes variables and returns the correct numeric answer.
    '''

    return [generate_answer(variables, formula) for _ in range(num)]


def value_of(name, variables):
    for v in variables:
        if v['name'] == name:
            return v['value']
    print('ERROR: No value for {}'.format(name))
    return None


if __name__ == '__main__':
    VARS = [{'name': 'x', 'min': 1.0, 'max': 10.0, 'scale': 0},
            {'name': 'y', 'min': 10.0, 'max': 20.0, 'scale': 0},
            {'name': 'z', 'min': 1.0, 'max': 20.0, 'scale': 0}]

    ANS = generate_answers(VARS, lambda vs: value_of('x', vs) + 1, 5)

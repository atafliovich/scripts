"""Module to help test student docstrings. Do not modify: use in your
own tester.

"""

import unittest
import doctest
import inspect
import re
import warnings
import inflect


from .messages import (EXISTS_FAILURE_MESSAGE,
                       FIRST_WORD_FAILURE_MESSAGE,
                       COMMAND_WORD_FAILURE_MESSAGE,
                       PARAM_FAILURE_MESSAGE, EXAMPLE_FAILURE_MESSAGE,
                       PARAM_ANNOTATION_FAILURE_MESSAGE,
                       RETURN_ANNOTATION_FAILURE_MESSAGE)

# keys for the settings dict
MODULE = 'module'
FUNC_TO_ANNOTATIONS = 'func_to_annotations'
COMMAND_WORDS = 'command_words'
FUNCTIONS_WITH_IO = 'functions_with_io'
NUM_EXAMPLES = 'num_examples'
ALLOW_THIRD_PERSON = 'allow_third_person'

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestDocstringsBase(unittest.TestCase):
    """Base class for testers of docstrings.
    """

    def exists_test(self, fname, settings):
        """Check that there is a function named fname with a docstring. If
        check succeeds, return (function, __doc__).

        """

        msg = EXISTS_FAILURE_MESSAGE.format(fname)

        # function exists
        if not hasattr(settings[MODULE], fname):
            self.fail(msg)

        func = getattr(settings[MODULE], fname)
        doc = func.__doc__

        # doc exists and is non-empty
        self.assertTrue(doc and doc.strip(), msg)

        return func, doc

    def first_word_test(self, fname, settings):
        """Check the first word of the docstring."""

        msg = FIRST_WORD_FAILURE_MESSAGE.format(fname)

        _, doc = self.exists_test(fname, settings)

        first_word = doc.split()[0].lower()
        is_command = first_word in settings[COMMAND_WORDS]

        if settings[ALLOW_THIRD_PERSON]:
            inflect_engine = inflect.engine()
            is_inflected_command = any(
                inflect_engine.compare_verbs(first_word, command_word)
                for command_word in settings[COMMAND_WORDS])

            self.assertTrue(is_inflected_command, msg)
        else:
            self.assertTrue(is_command, msg)

    def command_word_test(self, fname, settings):
        """Check that the docstring mentions at least one command word."""

        _, doc = self.exists_test(fname, settings)
        description_words = set(
            re.split(r'\W+', doc.split('>>>')[0].lower())) - {''}

        if settings[ALLOW_THIRD_PERSON]:
            inflect_engine = inflect.engine()
            contains_command_word = any(
                inflect_engine.compare_verbs(description_word, command_word)
                for description_word in description_words
                for command_word in settings[COMMAND_WORDS])
        else:
            contains_command_word = any(
                command_word in description_words
                for command_word in settings[COMMAND_WORDS])

        msg = COMMAND_WORD_FAILURE_MESSAGE.format(
            fname, settings[COMMAND_WORDS])
        self.assertTrue(contains_command_word, msg)

    def params_test(self, fname, settings):
        """Check that docstring mentions every parameter by name."""

        func, doc = self.exists_test(fname, settings)

        params = {p.lower() for p in inspect.signature(func).parameters}
        description_words = set(re.split(r'\W+', doc.split('>>>')[0].lower()))

        missing_params = params - description_words

        msg = PARAM_FAILURE_MESSAGE.format(fname, list(missing_params))

        self.assertTrue(missing_params == set(), msg)

    def num_examples_test(self, fname, settings):
        """Check that there are at least NUM_EXAMPLES examples in the
        docstring.

        """

        _, doc = self.exists_test(fname, settings)

        num_examples = len(doctest.DocTestParser().get_examples(doc))
        msg = EXAMPLE_FAILURE_MESSAGE.format(
            fname, settings[NUM_EXAMPLES], num_examples)

        self.assertTrue(num_examples >= settings[NUM_EXAMPLES], msg)

    def annotations_test(self, fname, settings):
        """Check correctness of annotations.

        Can split into two test cases: one for params and one for
        return?

        """

        func, _ = self.exists_test(fname, settings)

        expected_param = settings[FUNC_TO_ANNOTATIONS][fname][0]
        expected_return = settings[FUNC_TO_ANNOTATIONS][fname][1]
        sig = inspect.signature(func)
        param_annotations = [p.annotation
                             for p in sig.parameters.values()]
        return_annotation = sig.return_annotation

        param_msg = PARAM_ANNOTATION_FAILURE_MESSAGE.format(
            fname, expected_param, param_annotations)
        return_msg = RETURN_ANNOTATION_FAILURE_MESSAGE.format(
            fname, expected_return, return_annotation)

        self.assertEqual(param_annotations, expected_param, param_msg)
        self.assertEqual(return_annotation, expected_return, return_msg)


def auto_make_tests_from_functions(unittest_object, function_names, tests,
                                   settings, start_count=1):
    """Generate unittest test methods: one per function in function_names
    per method of TestDocstringsBase.

    """

    i = start_count
    for f_name in function_names:
        for test in tests:
            test_name = f'test_{i}_{test.__name__}_{f_name}'

            def new_test(self, fname=f_name, test=test, settings=settings):
                return test(self, fname, settings)
            # don't check examples in functions with IO
            if f_name not in settings[FUNCTIONS_WITH_IO]:
                setattr(unittest_object, test_name, new_test)
            i += 1

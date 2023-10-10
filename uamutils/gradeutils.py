"""Utilities to set up UAM.
"""

import os
import subprocess
import sys

from typing import TextIO

sys.path.append('/home/anya/scripts')  # NOQA: E402
from admin import students  # noqa
from admin import gradebook as gb  # noqa
from canvas import utils as canvasutils  # noqa

PYTHON = 'python3.11'
UAM_DIR = '/home/anya/at'
UAM_SUBMISSIONS_DIR = os.path.join(UAM_DIR, 'submissions')

DIRECTORIES = 'directories.txt'
DIRS_AND_NAMES = 'dirs_and_names.txt'
GROUPS = 'groups.txt'
CLASSLIST = 'classlist.csv'

STUDENTS = 'student'
TS = 'ta'


def setup_tester(course,
                 marking_dir: str,
                 local_dir: str,
                 target_group: str = STUDENTS):
    """Setup files that uam needs."""

    # write classlist for aggregator
    classlist_format = ('utorid', 'first', 'last', 'student_number', 'email')
    filename = canvasutils.write_classlist(
        course, marking_dir, classlist_format, True, target_group)

    try:
        os.remove(os.path.join(marking_dir, CLASSLIST))
    except FileNotFoundError:
        pass
    os.symlink(os.path.join(marking_dir, filename),
               os.path.join(marking_dir, CLASSLIST),
               target_is_directory=False)

    utorids = os.listdir(local_dir)

    directories = '\n'.join([os.path.join(local_dir, utorid)
                             for utorid in utorids])
    with open(DIRECTORIES, 'w', encoding='utf-8') as outfile:
        outfile.write(directories)

    dirs_and_names = '\n'.join(
        [f'{os.path.join(local_dir, utorid)},{utorid}'
         for utorid in utorids])
    with open(DIRS_AND_NAMES, 'w', encoding='utf-8') as outfile:
        outfile.write(dirs_and_names)

    groups_txt = '\n'.join([f'{utorid},{utorid},{utorid}'
                            for utorid in utorids])
    with open(GROUPS, 'w', encoding='utf-8') as outfile:
        outfile.write(groups_txt)


def setup_uam_links(marking_dir, local_dir):
    """Setup symlinks."""

    try:
        os.remove(UAM_SUBMISSIONS_DIR)
    except FileNotFoundError:
        pass

    os.symlink(os.path.join(marking_dir, local_dir),
               UAM_SUBMISSIONS_DIR,
               target_is_directory=True)


def run_all(marking_dir, config):
    """Run!"""

    os.chdir(UAM_DIR)
    print('Running test_runner...')
    exit_code = subprocess.call(
        [PYTHON, 'test_runner.py', f'{marking_dir}/{config}'])
    print(f'Done. Exit code {exit_code}')
    os.chdir(marking_dir)


def aggregate_all(assignment_name, marking_dir, result_files):
    """Aggregate."""

    os.chdir(UAM_DIR)
    print('Running aggregator(s)...')
    for result_file in result_files:
        print(f'\tAggregating {result_file}...')
        exit_code = subprocess.call(
            [PYTHON,
             'aggregator.py',
             assignment_name,
             os.path.join(marking_dir, DIRS_AND_NAMES),
             os.path.join(marking_dir, CLASSLIST),
             os.path.join(marking_dir, GROUPS),
             f'{result_file}.json',
             os.path.join(marking_dir,
                          f'{result_file}_aggregated.json')])
        print(f'Done. Exit code {exit_code}')
    os.chdir(marking_dir)


def template_all(marking_dir, result_files, txt=True, gf=True,
                 txt_template_file=None):
    """Template."""

    os.chdir(UAM_DIR)
    if txt:
        print('Running templator(s) all txt...')
        for result_file in result_files:
            print(f'\tTemplating all (txt) {result_file}...')
            exit_code = subprocess.call(
                [PYTHON,
                 'templator.py',
                 '-o',
                 result_file,
                 '--template_individual',
                 txt_template_file,
                 os.path.join(marking_dir, f'{result_file}_aggregated.json'),
                 'txt'])
            print(f'Done. Exit code {exit_code}.')

    if gf:
        print('Running templator(s) all gf...')
        for result_file in result_files:
            print(f'\tTemplating all (gf) {result_file}...')
            exit_code = subprocess.call(
                [PYTHON,
                 'templator.py',
                 '-a',
                 '-o',
                 os.path.join(marking_dir, result_file),
                 os.path.join(marking_dir, f'{result_file}_aggregated.json'),
                 'gf'])
            print(f'Done. Exit code {exit_code}.')
    os.chdir(marking_dir)


def gen_all(result_files, result_file_to_weigths):
    """result_file_to_weigths maps result-file-name.gf to weights-file-name.gf
    """

    print('Fixing up gf\'s.')

    for result_file in result_files:
        with open(f'{result_file}.gf', encoding='utf-8') as orig:
            content = orig.readlines()
        with open(result_file_to_weigths[result_file],
                  encoding='utf-8') as weights_file:
            weights = weights_file.readlines()

        content = (content[:content.index('\n') - 1] +
                   weights +
                   content[content.index('\n'):])

        with open(f'{result_file}.gf', 'w', encoding='utf-8') as newfile:
            newfile.write(''.join(content))

    for result_file in result_files:
        print(f'Running gen on {result_file}.gf...')
        exit_code = subprocess.call(['gen', f'{result_file}.gf'])
        print(f'Done. Exit code {exit_code}')


def run_one(utorid, marking_dir, config):
    """Run tester on one submission."""

    os.chdir(UAM_DIR)
    print(f'Running grade on {utorid}...')

    print(' '.join([PYTHON,
                    'grade.py',
                    os.path.join(marking_dir, DIRS_AND_NAMES),
                    os.path.join(marking_dir, config),
                    utorid]))

    exit_code = subprocess.call([PYTHON,
                                 'grade.py',
                                os.path.join(marking_dir, DIRS_AND_NAMES),
                                os.path.join(marking_dir, config),
                                utorid])
    print(f'Done. Exit code {exit_code}')
    os.chdir(marking_dir)


def template_one(utorid, marking_dir, local_dir, result_files, template_file):
    """Templator on one submission."""

    os.chdir(UAM_DIR)
    print(f'Running templator(s) txt (individual) on {utorid}...')
    for result_file in result_files:
        print(f'\tTemplating (txt) {result_file} for {utorid}...')
        exit_code = subprocess.call(
            [PYTHON,
             'templator.py',
             '-i',
             '-o',
             result_file,
             '--template_individual',
             template_file,
             os.path.join(marking_dir, local_dir, utorid,
                          f'{result_file}.json'),
             'txt'])
        print(f'Done. Exit code {exit_code}')
    os.chdir(marking_dir)


def test_all(marking_dir, local_dir, config, assignment_name,
             result_files, result_file_to_weigths,
             run=True, aggregate=True, template=True, gen=True,
             txt_template_file=None):
    """Run everything."""

    setup_uam_links(marking_dir, local_dir)

    if run:
        run_all(marking_dir, config)

    if aggregate:
        aggregate_all(assignment_name, marking_dir, result_files)

    if template:
        template_all(marking_dir, result_files, True, True,
                     txt_template_file)

    if gen:
        gen_all(result_files, result_file_to_weigths)


def test_one(utorid, marking_dir, local_dir, config, assignment_name,
             result_files, result_file_to_weigths,
             run=True, aggregate=True, template=True, gen=True,
             txt_template_file=None):
    """Test one submission."""

    setup_uam_links(marking_dir, local_dir)

    if run:
        run_one(utorid, marking_dir, config)

    if aggregate:
        aggregate_all(assignment_name, marking_dir, result_files)

    if template:
        template_one(utorid, marking_dir, local_dir,
                     result_files, txt_template_file)
        template_all(marking_dir, result_files, txt=False, gf=True,
                     txt_template_file=txt_template_file)

    if gen:
        gen_all(result_files, result_file_to_weigths)


def write_criteria_file(criteria: dict[str, float],
                        outfile: TextIO):
    """Write criteria.yml for upload to MarkUs.

    criteria maps criteria-name to out-of.

    Can't find a way to upload it with API... TODO.
    """

    format_str = '''{}:
  type: flexible
  max_mark: {}
  description: ''
  ta_visible: true
  peer_visible: false'''

    content = '\n'.join([format_str.format(name, outof)
                         for name, outof in criteria.items()])
    outfile.write(content + '\n')

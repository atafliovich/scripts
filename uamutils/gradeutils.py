import os
import subprocess
import sys

from typing import Dict, TextIO

sys.path.append('/home/anya/scripts')  # NOQA: E402
from admin import students  # noqa
from admin import gradebook as gb  # noqa
from canvas import utils as canvasutils  # noqa

PYTHON = 'python3.7'
UAM_DIR = '/home/anya/at'
UAM_SUBMISSIONS_DIR = os.path.join(UAM_DIR, 'submissions')

DIRECTORIES = 'directories.txt'
DIRS_AND_NAMES = 'dirs_and_names.txt'
GROUPS = 'groups.txt'
CLASSLIST = 'classlist.csv'


def setup_tester(course,
                 marking_dir: str,
                 local_dir: str):
    """Setup files that uam needs."""

    # write classlist for aggregator
    classlist_format = ('utorid', 'first', 'last', 'student_number', 'email')
    filename = canvasutils.write_classlist(
        course, marking_dir, classlist_format, True)

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
    with open(DIRECTORIES, 'w') as outfile:
        outfile.write(directories)

    dirs_and_names = '\n'.join(
        ['{},{}'.format(os.path.join(local_dir, utorid), utorid)
         for utorid in utorids])
    with open(DIRS_AND_NAMES, 'w') as outfile:
        outfile.write(dirs_and_names)

    groups_txt = '\n'.join(['{},{},{}'.format(utorid, utorid, utorid)
                            for utorid in utorids])
    with open(GROUPS, 'w') as outfile:
        outfile.write(groups_txt)


def setup_uam_links(marking_dir, local_dir):
    try:
        os.remove(UAM_SUBMISSIONS_DIR)
    except FileNotFoundError:
        pass

    os.symlink(os.path.join(marking_dir, local_dir),
               UAM_SUBMISSIONS_DIR,
               target_is_directory=True)


def run_all(marking_dir, config):
    os.chdir(UAM_DIR)
    print('Running test_runner...')
    exit_code = subprocess.call([PYTHON,
                                 'test_runner.py',
                                 '{}/{}'.format(marking_dir, config)])
    print('Done. Exit code {}'.format(exit_code))
    os.chdir(marking_dir)


def aggregate_all(assignment_name, marking_dir, result_files):
    os.chdir('/home/anya/at')
    print('Running aggregator(s)...')
    for result_file in result_files:
        print('\tAggregating {}...'.format(result_file))
        exit_code = subprocess.call(
            [PYTHON,
             'aggregator.py',
             assignment_name,
             os.path.join(marking_dir, DIRS_AND_NAMES),
             os.path.join(marking_dir, CLASSLIST),
             os.path.join(marking_dir, GROUPS),
             '{}.json'.format(result_file),
             os.path.join(marking_dir,
                          '{}_aggregated.json'.format(result_file))])
        print('Done. Exit code {}'.format(exit_code))
    os.chdir(marking_dir)


def template_all(marking_dir, result_files, txt=True, gf=True):
    os.chdir('/home/anya/at')
    if txt:
        print('Running templator(s) all txt...')
        for result_file in result_files:
            print('\tTemplating all (txt) {}...'.format(result_file))
            exit_code = subprocess.call(
                [PYTHON,
                 'templator.py',
                 '-o',
                 result_file,
                 os.path.join(
                     marking_dir, '{}_aggregated.json'.format(result_file)),
                 'txt'])
            print('Done. Exit code {}'.format(exit_code))

    if gf:
        print('Running templator(s) all gf...')
        for result_file in result_files:
            print('\tTemplating all (gf) {}...'.format(result_file))
            exit_code = subprocess.call(
                [PYTHON,
                 'templator.py',
                 '-a',
                 '-o',
                 os.path.join(marking_dir, result_file),
                 os.path.join(
                     marking_dir, '{}_aggregated.json'.format(result_file)),
                 'gf'])
            print('Done. Exit code {}'.format(exit_code))
    os.chdir(marking_dir)


def gen_all(result_files, result_file_to_weigths):
    """result_file_to_weigths maps result-file-name.gf to weights-file-name.gf
    """

    print('Fixing up gf\'s.')

    for result_file in result_files:
        with open('{}.gf'.format(result_file)) as orig:
            content = orig.readlines()
        with open(result_file_to_weigths[result_file]) as weights_file:
            weights = weights_file.readlines()

        content = (content[:content.index('\n') - 1] +
                   weights +
                   content[content.index('\n'):])

        with open('{}.gf'.format(result_file), 'w') as newfile:
            newfile.write(''.join(content))

    for result_file in result_files:
        print('Running gen on {}.gf...'.format(result_file))
        exit_code = subprocess.call(['gen', '{}.gf'.format(result_file)])
        print('Done. Exit code {}'.format(exit_code))


def run_one(utorid, marking_dir, config):
    os.chdir(UAM_DIR)
    print('Running grade on {}...'.format(utorid))
    exit_code = subprocess.call([PYTHON,
                                 'grade.py',
                                 os.path.join(marking_dir, DIRS_AND_NAMES),
                                 os.path.join(marking_dir, config),
                                 utorid])
    print('Done. Exit code {}'.format(exit_code))
    os.chdir(marking_dir)


def template_one(utorid, marking_dir, local_dir, result_files):
    os.chdir(UAM_DIR)
    print('Running templator(s) txt (individual) on {}...'.format(utorid))
    for result_file in result_files:
        print('\tTemplating (txt) {} for {}...'.format(result_file, utorid))
        exit_code = subprocess.call(
            [PYTHON,
             'templator.py',
             '-i',
             '-o',
             result_file,
             os.path.join(marking_dir, local_dir, utorid,
                          '{}.json'.format(result_file)),
             'txt'])
        print('Done. Exit code {}'.format(exit_code))
    os.chdir(marking_dir)


def test_all(marking_dir, local_dir, config, assignment_name,
             result_files, result_file_to_weigths,
             run=True, aggregate=True, template=True, gen=True):

    setup_uam_links(marking_dir, local_dir)

    if run:
        run_all(marking_dir, config)

    if aggregate:
        aggregate_all(assignment_name, marking_dir, result_files)

    if template:
        template_all(marking_dir, result_files, True, True)

    if gen:
        gen_all(result_files, result_file_to_weigths)


def test_one(utorid, marking_dir, local_dir, config, assignment_name,
             result_files, result_file_to_weigths,
             run=True, aggregate=True, template=True, gen=True):
    """Test one submission."""

    setup_uam_links(marking_dir, local_dir)

    if run:
        run_one(utorid, marking_dir, config)

    if aggregate:
        aggregate_all(assignment_name, marking_dir, result_files)

    if template:
        template_one(utorid, marking_dir, local_dir, result_files)
        template_all(marking_dir, result_files, txt=False, gf=True)

    if gen:
        gen_all(result_files, result_file_to_weigths)


def write_criteria_file(criteria: Dict[str, float],
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

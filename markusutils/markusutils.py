""" Work with MarkUs.
"""

import os
import sys
from typing import TextIO
import markusapi

# TODO: will remove for proper local install
sys.path.append('/home/anya/scripts')  # NOQA: E402
from admin import gradebook as gb  # noqa


def get_submissions(api: markusapi.Markus, course_id: int,
                    assignment_id: int, markus_files: list[str],
                    local_dir: str, local_files: list[str],
                    utorids: list[str] = None):
    """Download all submissions for assignment_id and store them locally.

    If markus_files is None, then download a zip file of entire
    submission. The name of the local zip file must be specified in
    local_files[0].

    markus_files: names/paths of the files on MarkUs, for each
      student, to download.
    local_dir, local_files: write files locally in local_dir/utorid/local_file,
             for each student (utorid).

    """

    groups = api.get_groups(course_id, assignment_id)

    for group in groups:
        group_id, utorid = group['id'], group['group_name']

        if utorids is None or utorid in utorids:
            get_submission(api, course_id, assignment_id, markus_files,
                           local_dir, local_files, utorid, group_id)


def get_submission(api: markusapi.Markus, course_id: int,
                   assignment_id: int, markus_files: list[str],
                   local_dir: str, local_files: list[str], utorid,
                   group_id=None):
    """Download one submission for assignment_id and store it locally.
    TODO: rethink?

    If markus_files is None, then download a zip file of entire
    submission. The name of the local zip file must be specified in
    local_files[0].

    markus_files: names of the files on MarkUs to download.
    local_dir, local_files: write files locally in local_dir/utorid/local_file.

    if group_id is None, download groups from MarkUs and find the group_id.

    """

    if group_id is None:
        try:
            group_id = _get_group_id(api, course_id, assignment_id, utorid)
        except NoMarkUsGroupError as error:
            print(error)
            return

    path = os.path.join(local_dir, utorid)
    print(f'Making dir {path}')
    os.makedirs(path, 0o711, True)

    if markus_files is None:
        _get_one_file(api, course_id, assignment_id, group_id, utorid,
                      None, local_dir, local_files[0])
        return

    for i, fle in enumerate(markus_files):
        _get_one_file(api, course_id, assignment_id, group_id, utorid,
                      fle, local_dir, local_files[i])


def _get_one_file(api, course_id, assignment_id, group_id, utorid,
                  markus_file, local_dir, local_file):

    # last arg is True: download collected version from repo
    # last arg is False: download the latest version from repo
    # markus_file is None: download a zip file of entire submission
    contents = api.get_files_from_repo(course_id, assignment_id,
                                       group_id, markus_file, True)

    if isinstance(contents, dict):
        print(f'Warning: no submission for {utorid}:',
              str(contents.get('status', contents.get('code', ''))) + ':',
              str(contents.get('error', contents.get('description', '')))
              + '.')
        return

    path = os.path.join(local_dir, utorid, local_file)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb') as outfile:
        outfile.write(contents)


def upload_result_files(api: markusapi.Markus, course_id: int,
                        assignment_id: int, local_dir: str,
                        result_file_name: str, utorids: list[str] = None):
    """Upload local_dir/utorid/result_file_name into each student repo on
    MarkUs.

    """

    groups = api.get_groups(course_id, assignment_id)

    for group in groups:
        group_id, utorid = group['id'], group['group_name']

        if utorids is None or utorid in utorids:
            upload_result_file(api, course_id, assignment_id, local_dir,
                               result_file_name, utorid, group_id)


def upload_result_file(api: markusapi.Markus, course_id: int,
                       assignment_id: int, local_dir: str,
                       result_file_name: str, utorid: str,
                       group_id: int = None):
    """Upload local_dir/utorid/result_file_name into the student repo on
    MarkUs.

    if group_id is None, download groups from MarkUs and find the group_id.
    """

    if group_id is None:
        try:
            group_id = _get_group_id(api, course_id, assignment_id, utorid)
        except NoMarkUsGroupError as error:
            print(error)
            return

    result_file_path = os.path.join(local_dir, utorid, result_file_name)
    try:
        with open(result_file_path, encoding='utf-8') as result_file:
            contents = result_file.read()
    except FileNotFoundError:
        print(f'Warning: no result file for {utorid}.')
        return

    response = api.upload_file_to_repo(course_id, assignment_id,
                                       group_id, result_file_name,
                                       contents)
    # 201 is success
    if response.get('status', 0) == 500 or response.get('code', 0) != '201':
        print(f'Could not upload result file for {utorid}: {response}.')


def upload_grades(api: markusapi.Markus, course_id: int,
                  assignment_id: int, gf_file: TextIO, criteria:
                  dict[str, tuple[str, float]], complete=True):
    """Upload grades.

    criteria maps test-name-in-gf-file to (criteria-name, out-of) on MarkUs.

    criteria on MarkUs needs to be set up beforehand. Can't find a way
    to upload it with API... TODO.
    if complete, set MarkUs submission status to "complete"

    """

    gbook = gb.GradeBook.load_gf_file(gf_file, 'utorid', True)

    groups = api.get_groups(course_id, assignment_id)

    for group in groups:
        group_id, utorid = group['id'], group['group_name']
        upload_grade(api, course_id, assignment_id, criteria, utorid,
                     gbook, None, group_id, complete)


def upload_grade(api: markusapi.Markus,
                 course_id: int,
                 assignment_id: int,
                 criteria: dict[str, tuple[str, float]],
                 utorid: str,
                 gbook: gb.GradeBook = None,
                 gf_file: TextIO = None,
                 group_id: int = None,
                 complete=True):
    """Upload grades for one student.

    criteria maps test-name-in-gf-file to (criteria-name, out-of) on MarkUs.

    criteria on MarkUs needs to be set up beforehand. Can't find a way
    to upload it with API... TODO.

    if gbook is None, reload from gf_file
    if group_id is None, download group info from MarkUs.
    if complete, set MarkUs submission status to "complete"
    """

    if group_id is None:
        try:
            group_id = _get_group_id(api, course_id, assignment_id, utorid)
        except NoMarkUsGroupError as error:
            print(error)
            return

    if gbook is None:
        gbook = gb.GradeBook.load_gf_file(gf_file, 'utorid', True)
    try:
        grades = gbook.get_student_grades_by_utorid(utorid)
        criteria_mark_map = {criteria[test_name][0]:
                             grades.get_grade(test_name) *
                             criteria[test_name][2] /
                             criteria[test_name][1]
                             for test_name in criteria}
    except Exception as exn:  # no grade for this student
        print(f'Warning: no grades info for {utorid}. Uploading 0. ({exn})')
        criteria_mark_map = {name: 0 for (name, _, _) in
                             criteria.values()}

    # HACK: undo complete state
    api.update_marking_state(course_id, assignment_id, group_id,
                             'incomplete')

    response = api.update_marks_single_group(
        course_id, criteria_mark_map, assignment_id, group_id)

    # 200 is success
    if response.get('status', 0) == 500 or response.get('code', 0) != '200':
        print(f'Could not upload grades for {utorid}: {response}.')
        return

    if complete:
        response = api.update_marking_state(course_id, assignment_id,
                                            group_id, 'complete')
    # 200 is success
    if response.get('status', 0) == 500 or response.get('code', 0) != '200':
        print(f'Could not set state to complete for {utorid}: {response}.')


def get_utorid_to_group(api: markusapi.Markus, course_id: int,
                        assignment_id: int) -> dict[str, dict]:
    """Return a mapping from utroid to MarkUs group record."""

    return {group['group_name']: group
            for group in api.get_groups(course_id, assignment_id)}


def _get_group_id(api: markusapi.Markus, course_id: int,
                  assignment_id: int, utorid: str) -> int:
    """Raises NoMarkUsGroupError if no such student."""

    utorid_to_group = get_utorid_to_group(api, course_id, assignment_id)
    try:
        return utorid_to_group[utorid]['id']
    except KeyError as exc:
        raise NoMarkUsGroupError(
            f'Error: no MarkUs group for {utorid}.') from exc


class NoMarkUsGroupError(Exception):
    pass

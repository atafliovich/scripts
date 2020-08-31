'''Working with GitHub.
'''

from github import GithubException


def add_tas_to_repos(ta_to_repos, github, org):
    '''Add TAs to team repos.

    ta_to_repos maps TA git username to List of repo names.
    github is an object returned by github.GitHub
    org is a github.Organization

    '''

    for ta, repos in ta_to_repos.items():

        try:
            user = github.get_user(ta)
        except GithubException:
            print('No user {}.'.format(ta))
            continue

        for reponame in repos:
            try:
                repo = org.get_repo(reponame)
            except GithubException:
                print('No repo {}.'.format(reponame))
                continue

            repo.add_to_collaborators(user, permission='push')


def setup_team_repos(teams, github, org):
    '''Set up teams and project repositories.
    teams is a file in format team_name, gitusername1, gitusername2, ...
    github is an object returned by github.GitHub
    org is a github.Organization
    '''

    for team, students in teams.items():
        reponame = '{}-project'.format(team)
        try:
            repo = org.create_repo(
                reponame,
                description="{} project repository".format(team),
                private=True)
        except GithubException:
            print('Cannot create repo for {}.'.format(team))
            continue

        try:
            git_team = org.create_team(
                team, repo_names=[repo], permission='push', privacy='closed',
                description='CSCC01 Project Team')
        except GithubException:
            print('Cannot create team {}.'.format(team))
            continue

        for student in students:
            try:
                user = github.get_user(student.gitid)
            except GithubException:
                print('No user {}.'.format(student.gitid))
                continue

            git_team.add_membership(user)


def setup_exercise_repos(students, ex, github, org, debug=False):
    '''Set up exercise repositories.
    students is a Students.
    ex is the name of the exercise.
    github is an object returned by github.GitHub
    org is a github.Organization
    '''

    for student in students:
        username = student.gitid
        reponame = '{}-{}'.format(username, ex)

        if debug:
            print('Setting up repo {}'.format(reponame))

        try:
            user = github.get_user(username)
        except GithubException:
            print('No user {}.'.format(username))
            continue

        try:
            repo = org.create_repo(
                reponame,
                description="{} {} repository".format(username, ex),
                private=True)
        except GithubException:
            print('Cannot create repo for {}.'.format(username))
            continue

        repo.add_to_collaborators(user, permission='push')


def setup_exam_repos(students, ex, org, debug=False):
    '''Set up exam repositories. Note: students will not have access to these repos.

    students is a Students.
    ex is the name of the exam.
    org is a github.Organization
    '''

    for student in students:
        username = student.gitid
        reponame = '{}-{}'.format(username, ex)

        if debug:
            print('Setting up repo {}'.format(reponame))

        try:
            org.create_repo(
                reponame,
                description="{} {} repository".format(username, ex),
                private=True)
        except GithubException:
            print('Cannot create repo for {}.'.format(username))
            continue


def open_exam_repos(students, ex, github, org, debug=False):
    '''Open exam repositories for students (grant permissions).

    students is a Students.
    ex is the name of the exam.
    github is an object returned by github.GitHub
    org is a github.Organization
    '''

    for student in students:
        username = student.gitid
        reponame = '{}-{}'.format(username, ex)

        if debug:
            print('Setting up repo {}'.format(reponame))

        try:
            user = github.get_user(username)
        except GithubException:
            print('No user {}.'.format(username))
            continue

        try:
            repo = org.get_repo(reponame)
        except GithubException:
            print('No repo {}.'.format(reponame))
            continue

        repo.add_to_collaborators(user, permission='push')


def push_starter(filepaths, students, message, repo_format_str, org, branch=None, debug=False):
    """Push starter code to student repositories.

    filepaths -- iterable of paths to the files that will be pushed.
       These are both local paths for getting the contents of
       the files, and the remote paths, relative to the root of the
       repository (dirs that do not exist will be created).
    students -- a Students object
    message -- commit message
    repo_format_str -- specifies the repo name for each student:
         the repo name will be repo_format_str.format(gitid)
    org -- github organisation
    branch -- branch in repo to push to

    """

    for filepath in filepaths:
        with open(filepath) as infile:
            content = infile.read()
        push_file(students, filepath, message, content,
                  repo_format_str, org, branch, debug)


def push_file(students, path, message, content,
              repo_format_str, org, branch=None, debug=False):
    '''Push file into a repo of every student.
    students -- a Students object
    path -- path to the new file in the repo (dirs that do not exist will be created)
    message -- commit message
    content -- content of the new file
    repo_format_str -- specifies the repo name for each student:
         the repo name will be repo_format_str.format(gitid)
    org -- github organisation
    branch -- branch in repo to push to
    '''

    for student in students:
        username = student.gitid
        reponame = repo_format_str.format(username)

        if debug:
            print('Setting up starter for {}'.format(reponame))

        try:
            repo = org.get_repo(reponame)
        except GithubException:
            print('No repo {}.'.format(reponame))
            continue

        # TODO: fix hack. What is this default NotSet for branch?
        try:
            if branch:
                repo.create_file(path, message, content, branch)
            else:
                repo.create_file(path, message, content)
        except GithubException:
            print('Cannot push file {}.'.format(path))
            continue


def create_issues(students, title, body, repo_format_str, org, debug=False):
    '''Create issue in the repo of every student.

    students -- a Students object
    title -- title of the issue
    body -- body text of hte issue
    repo_format_str -- specifies the repo name for each student:
         the repo name will be repo_format_str.format(gitid)
    org -- github organisation
    '''

    for student in students:
        username = student.gitid
        reponame = repo_format_str.format(username)

        if debug:
            print('Creating issue for repo {}'.format(reponame))

        try:
            repo = org.get_repo(reponame)
        except GithubException:
            print('No repo {}.'.format(reponame))
            continue

        repo.create_issue(title, body=body, assignee=student.gitid)

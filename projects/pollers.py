from kwextensions.changes import GitlabMergeRequestPoller, GitlabIntegrationBranchPoller

import geojs.poll

__all__ = [
    'make_pollers',
]


REPOS = []
BRANCHES = {}
CDASH_INFO = {}


def _add_project_poll(poll):
    global REPOS
    REPOS.append(poll.REPO)

    global BRANCHES
    BRANCHES[poll.REPO] = poll.BRANCHES

    global CDASH_INFO
    CDASH_INFO[poll.REPO] = (poll.CDASH_ROOT, poll.CDASH_PROJECTNAME)


# VTK
_add_project_poll(geojs.poll)


def make_pollers(secrets):

    pollers = [
    ]

    return pollers

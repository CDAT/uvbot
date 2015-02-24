from kwextensions.changes import GitlabMergeRequestPoller, GitlabIntegrationBranchPoller

import paraview.poll
import paraviewsuperbuild.poll


__all__ = [
    'make_pollers',
]


REPOS = []
BRANCHES = {}


def _add_project_poll(poll):
    global REPOS
    REPOS.append(poll.REPO)

    global BRANCHES
    BRANCHES[poll.REPO] = poll.BRANCHES


_add_project_poll(paraview.poll)
_add_project_poll(paraviewsuperbuild.poll)


def make_pollers(secrets):
    pollers = [
        # Poll for merge requests.
        GitlabMergeRequestPoller(
            rooturl=secrets['gitlab_rooturl'],
            token=secrets['gitlab_api_token'],
            projects=REPOS,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True),

        # Poll for changes to the integration branches.
        GitlabIntegrationBranchPoller(
            rooturl=secrets['gitlab_rooturl'],
            token=secrets['gitlab_api_token'],
            projects=BRANCHES,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True),
    ]

    return pollers

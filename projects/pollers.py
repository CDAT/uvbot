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
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            projects=REPOS,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True),

        # Poll for changes to the integration branches.
        GitlabIntegrationBranchPoller(
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            projects=BRANCHES,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True),
    ]

    return pollers

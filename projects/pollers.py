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
        # Poll for merge requests.
        GitlabMergeRequestPoller(
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            web_host=secrets['web_status_url'],
            projects=REPOS,
            cdash_info=CDASH_INFO,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True,
            forceLowerCase=False),

        # Poll for changes to the integration branches.
        GitlabIntegrationBranchPoller(
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            projects=BRANCHES,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=True,
            forceLowerCase=False),
    ]

    return pollers

from kwextensions.changes import GitlabMergeRequestPoller, GitlabIntegrationBranchPoller

# VTK
import vtk.poll

# ParaView
import paraview.poll
import paraviewsuperbuild.poll


__all__ = [
    'make_pollers',
]


REPOS = []
BRANCHES = {}
CDASH_PROJECTNAMES = {}


def _add_project_poll(poll):
    global REPOS
    REPOS.append(poll.REPO)

    global BRANCHES
    BRANCHES[poll.REPO] = poll.BRANCHES

    global CDASH_PROJECTNAMES
    CDASH_PROJECTNAMES[poll.REPO] = poll.CDASH_PROJECTNAME


# VTK
_add_project_poll(vtk.poll)

# ParaView
_add_project_poll(paraview.poll)
_add_project_poll(paraviewsuperbuild.poll)


def make_pollers(secrets):
    pollers = [
        # Poll for merge requests.
        GitlabMergeRequestPoller(
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            web_host=secrets['web_status_url'],
            projects=REPOS,
            cdash_host=secrets['cdash_url'],
            cdash_projectnames=CDASH_PROJECTNAMES,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=False),

        # Poll for changes to the integration branches.
        GitlabIntegrationBranchPoller(
            host=secrets['gitlab_host'],
            token=secrets['gitlab_api_token'],
            projects=BRANCHES,
            cdash_host=secrets['cdash_url'],
            cdash_projectnames=CDASH_PROJECTNAMES,
            verify_ssl=False,
            pollInterval=10*60, # in seconds
            pollAtLaunch=False),
    ]

    return pollers

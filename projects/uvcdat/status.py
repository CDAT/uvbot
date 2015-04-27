from kwextensions.github_status2 import GitHubStatus
from buildbot.process.properties import Interpolate


def make_project_status(secrets):
    """Respond using github's status api."""
    # doesn't seem to work right:
    return GitHubStatus(
        token=secrets['github_status_token'],  # Generate using your user settings->applications in github
        repoOwner=Interpolate('%(prop:github_owner)s'),
        repoName=Interpolate('%(prop:github_repo)s'),
        sha=Interpolate('%(src::revision)s'),
        startDescription='Build started'
    )

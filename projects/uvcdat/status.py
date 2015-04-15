from buildbot.status.github import GitHubStatus
from buildbot.process.properties import Interpolate


def make_project_status(secrets):
    """Respond using github's status api."""
    # doesn't seem to work right:
    return GitHubStatus(
        token=secrets['github_status_token'],  # Generate using your user settings->applications in github
        repoOwner='UV-CDAT',
        repoName='uvcdat',
        sha=Interpolate('%(src::revision)s'),
        startDescription='Build started'
    )

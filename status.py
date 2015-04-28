from buildbot.status import html
from buildbot.status.web import authz, auth
from kwextensions.github_status2 import GitHubStatus
from buildbot.process.properties import Interpolate


__all__ = [
    'make_web_status',
]


def make_web_status(secrets):
    authz_cfg = authz.Authz(
        # change any of these to True to enable; see the manual for more
        # options
        auth=auth.HTPasswdAprAuth('%s/webstatuspasswords' % secrets['buildbot_root']),
        gracefulShutdown=False,
        forceBuild='auth', # use this to test your slave once it is set up
        forceAllBuilds='auth',  # ..or this
        pingBuilder=False,
        stopBuild='auth',
        stopAllBuilds='auth',
        cancelPendingBuild='auth',
    )

    return [
        html.WebStatus(
            http_port=secrets['web_status_port'],
            authz=authz_cfg,
            change_hook_dialects={
                'github': True
            }
        ),
        GitHubStatus(
            token=secrets['github_status_token'],  # Generate using your user settings->applications in github
            repoOwner=Interpolate('%(prop:github_owner)s'),
            repoName=Interpolate('%(prop:github_repo)s'),
            sha=Interpolate('%(src::revision)s'),
            startDescription='Build started'
        ),
    ]

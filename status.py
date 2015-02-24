from buildbot.status import html
from buildbot.status.web import authz, auth


__all__ = [
    'make_web_status',
]


def make_web_status(secrets, dashdir=None):
    authz_cfg = authz.Authz(
        # change any of these to True to enable; see the manual for more
        # options
        auth=auth.HTPasswdAprAuth('%s/webstatuspasswords' % dashdir),
        gracefulShutdown=False,
        forceBuild='auth', # use this to test your slave once it is set up
        forceAllBuilds='auth',  # ..or this
        pingBuilder=False,
        stopBuild='auth',
        stopAllBuilds='auth',
        cancelPendingBuild='auth',
    )

    return html.WebStatus(
        http_port=secrets['web_status_port'],
        authz=authz_cfg
    )

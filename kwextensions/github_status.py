"""Build steps to set statuses on Github projects."""

from buildbot.steps.http import POST
from buildbot.process.properties import Interpolate


def post_github_status(repo, state, token, **kw):
    """Post a status to a commit on github.

    Note this function requires the python package `txrequests` and `requests`.

    :param repo: The repository name i.e. (kitware/VTK)
    :param state: The status (pending, success, error, failure)
    :param token: An oauth key with status permissions

        see your user settings -> applications in github

    Optional parameters are as follows:

    :param url: The target url when the user clicks the status icon
    :param description: Short description of the status.
    :param context: A unique context for the status (default kitware/buildbot)
    :param sha: The sha to attach the status to (default "%(src::revision)s")
    :param apiroot: default https://api.github.com """
    params = {
        'state': state,
        'context': kw.get('context', 'kitware/buildbot')
    }
    if kw.get('url'):
        params['url'] = kw['url']

    if kw.get('description'):
        params['description'] = kw['description']

    sha = kw.get('sha', Interpolate('%(src::revision)s'))
    api = kw.get('apiroot', 'https://api.github.com').rstrip('/')

    return POST(
        url='/'.join((api, 'repos', repo, 'statuses', sha)),
        data=params,
        auth=(token, 'x-oauth-basic')
    )

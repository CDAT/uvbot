from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll
from projects.paraview.poll import REPO as PARAVIEW_REPO
import urllib

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    # Setup defaults to use for all the codebases.
    # Note, this also acts as a change filter and hence must
    # include defaults for all relevant codebases.
    codebases = {
        PARAVIEW_REPO : {
            "repository" : "%s/%s" % (secrets['gitlab_host'], urllib.quote(PARAVIEW_REPO.lower(), '')),
            "branch" : "master",
            "revision" : None,
            },
        poll.REPO : {
            "repository" : "%s/%s" % (secrets['gitlab_host'], urllib.quote(poll.REPO.lower(), '')),
            "branch" : "master",
            "revision" : None,
            },
        }

    return [
        AnyBranchScheduler(
            name='ParaViewSuperbuild Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'merge-request' created/changed.",
            # For superbuilds, merge requets on superbuild itself should always
            # trigger a clean build, I suppose.
            properties={ "ctest_empty_binary_directory" : True },
            codebases=codebases),
        AnyBranchScheduler(
            name='ParaViewSuperbuild Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'master' changed.",
            properties={ "ctest_empty_binary_directory" : True },
            codebases=codebases),
        AnyBranchScheduler(
            name='ParaViewSuperbuild ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=PARAVIEW_REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            properties={ "ctest_empty_binary_directory" : True },
            codebases=codebases),
    ]

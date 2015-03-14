from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll
from projects.paraview.poll import REPO as PARAVIEW_REPO

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames):
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
            properties={ "ctest_empty_binary_directory" : True }),
        AnyBranchScheduler(
            name='ParaViewSuperbuild Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'master' changed.",
            properties={ "ctest_empty_binary_directory" : True }),
        AnyBranchScheduler(
            name='ParaViewSuperbuild ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=PARAVIEW_REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            properties={ "ctest_empty_binary_directory" : True }),
    ]

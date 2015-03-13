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
            reason="ParaViewSuperbuild 'merge-request' created/changed."),
        AnyBranchScheduler(
            name='ParaViewSuperbuild Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'master' changed."),
        AnyBranchScheduler(
            name='ParaViewSuperbuild ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=PARAVIEW_REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed."),
    ]

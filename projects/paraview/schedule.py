from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll


__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    return [
        AnyBranchScheduler(
            name='ParaView Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'merge-request' created/changed.",
            codebases={poll.REPO: {}}),
        AnyBranchScheduler(
            name='ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            properties={ "ctest_empty_binary_directory" : True },
            codebases={poll.REPO: {}}),
    ]

from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll
import projects
from projects import paraview
from projects.paraview.poll import REPO as PARAVIEW_REPO

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    # Setup defaults to use for all the codebases.
    # Note, this also acts as a change filter and hence must
    # include defaults for all relevant codebases.
    codebases = {}
    codebases.update(projects.get_codebase(project=paraview, secrets=secrets))
    codebases.update(projects.get_codebase(poll=poll, secrets=secrets))
    return [
        AnyBranchScheduler(
            name='ParaViewSuperbuild Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'merge-request' created/changed.",
            properties={
                # For superbuilds, merge requets on superbuild itself should always
                # trigger a clean build, I suppose.
                "ctest_empty_binary_directory" : True,
                "ctest_track" : "buildbot-packages",
                },
            codebases=codebases),
        AnyBranchScheduler(
            name='ParaViewSuperbuild Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaViewSuperbuild 'master' changed.",
            properties={
                "ctest_empty_binary_directory" : True,
                "ctest_track" : "master-packages",
                },
            codebases=codebases),
        AnyBranchScheduler(
            name='ParaViewSuperbuild ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=PARAVIEW_REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            properties={
                "ctest_empty_binary_directory" : True,
                "ctest_track" : "master-packages",
                },
            codebases=codebases),
    ]

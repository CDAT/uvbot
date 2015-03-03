from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler, ChoiceStringParameter, UserNameParameter, FixedParameter
from buildbot.changes import filter


from . import poll


__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames):
    return [
        AnyBranchScheduler(
            name='ParaView-Catalyst Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames),
        AnyBranchScheduler(
            name='ParaView-Catalyst Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames),
        ForceScheduler(
            name='Force Build Catalyst',
            builderNames=buildnames,
            branch=FixedParameter(name='branch', default='master'),
            username=UserNameParameter(label='your name:<br>', size=80),
            project=FixedParameter(name='project',default='Catalyst'),
            revision=FixedParameter(name='revision',default=''),
            repository=FixedParameter(name='repository',
                 default='https://kwgitlab.kitwarein.com/paraview/paraview.git'),
            ),
    ]

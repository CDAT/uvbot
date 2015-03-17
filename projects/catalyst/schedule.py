from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler, ChoiceStringParameter, UserNameParameter, FixedParameter, StringParameter
from buildbot.changes import filter
import urllib

from . import poll
import projects

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    codebases = projects.get_codebase(poll=poll, secrets=secrets)
    return [
        AnyBranchScheduler(
            name='ParaView-Catalyst Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'merge-request' created/changed.",
            codebases=codebases,
            properties={
                'ctest_track': "buildbot-catalyst-editions",
                },
            ),
        AnyBranchScheduler(
            name='ParaView-Catalyst Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            codebases=codebases,
            properties={
                'ctest_track': "master-catalyst-editions",
                },
            ),
        ForceScheduler(
            name='Force Build Catalyst',
            builderNames=buildnames,
            username=UserNameParameter(label='your name:<br>', size=80),
            codebases=codebases,
            properties=[
                StringParameter(name="ctest_track",
                    label="Dashboard track",
                    default="buildbot-catalyst-editions",
                    size=30)
                ],
            ),
    ]

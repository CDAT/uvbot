from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.timed import Nightly
from buildbot.changes import filter


from . import poll
import projects

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    codebases = projects.get_codebase(poll=poll, secrets=secrets)
    return [
        AnyBranchScheduler(
            name='ParaView Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO,
                filter_fn=projects.get_change_filter_fn_for_buildbot_commands(accepted_values=['test'])
            ),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'merge-request' created/changed.",
            codebases=codebases,
            properties={
                'ctest_track': 'buildbot-paraview',
            }),
        AnyBranchScheduler(
            name='ParaView Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="ParaView 'master' changed.",
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'master',
            }),
        Nightly(
            name='ParaView Weekly Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            branch='master',
            dayOfWeek=6, # Saturday
            hour=23, # 11pm
            onlyIfChanged=False,
            builderNames=buildnames,
            reason='Weekly test exclusion check.',
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'master',
                'ignore_exclusions': True,
            }),
    ]

from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.timed import Nightly


__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    return [
        AnyBranchScheduler(
            name='UV-CDAT Branch Change Scheduler',
            treeStableTimer=300,
            builderNames=buildnames,
            reason="UV-CDAT repository changed.",
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Experimental',
            },
            branches=['master', 'buildbot-test']
            ),
        Nightly(
            name='UV-CDAT Nightly Scheduler',
            branch='master',
            hour=22,
            onlyIfChanged=False,
            builderNames=buildnames,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Nightly',
                'ignore_exclusions': True,
            }
        )
    ]

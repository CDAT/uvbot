from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.timed import Nightly


from . import poll
import projects

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    codebases = projects.get_codebase(poll=poll, secrets=secrets)
    return [
        AnyBranchScheduler(
            name='UV-CDAT Branch Change Scheduler',
            treeStableTimer=300,
            builderNames=buildnames,
            reason="GeoJS repository changed.",
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Experimental',
            },
            branches=['master']
            ),
        Nightly(
            name='UV-CDAT Nightly Scheduler',
            branch='master',
            hour=22,
            onlyIfChanged=False,
            builderNames=buildnames,
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Nightly',
                'ignore_exclusions': True,
            }
        )
    ]

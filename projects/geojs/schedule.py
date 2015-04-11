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
            name='GeoJS Branch Change Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason="GeoJS 'master' changed.",
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Experimental',
            }),
        Nightly(
            name='GeoJS Nightly Scheduler',
            branch='master',
            hour=23,
            onlyIfChanged=False,
            builderNames=buildnames,
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Nightly',
                'ignore_exclusions': True,
            }),
    ]

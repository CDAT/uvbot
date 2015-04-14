from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.timed import Nightly
from buildbot.changes import filter


__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    return [
        AnyBranchScheduler(
            name='GeoJS Branch Change Scheduler',
            treeStableTimer=300,
            builderNames=buildnames,
            reason="GeoJS repository changed.",
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Experimental',
            },
            change_filter=filter.ChangeFilter(
                repository_re=r'.*geojs\.git.*'
            )),
        Nightly(
            name='GeoJS Nightly Scheduler',
            branch='master',
            hour=23,
            onlyIfChanged=False,
            builderNames=buildnames,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'Nightly',
                'ignore_exclusions': True,
            },
            change_filter=filter.ChangeFilter(
                repository_re=r'.*geojs\.git.*'
            )),
    ]

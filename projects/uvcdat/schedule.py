from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.timed import Nightly
from buildbot.changes import filter
from buildbot.schedulers.forcesched import ForceScheduler, \
        ChoiceStringParameter, FixedParameter, StringParameter


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
            change_filter=filter.ChangeFilter(
                repository_re=r'.*/uvcdat$'
            )
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
        ),
        ForceScheduler(
            name='force-uvcdat',
            builderNames=buildnames,
            reason=FixedParameter(
                name="reason",
                default="UV-CDAT build triggered manually."
            ),
            branch=StringParameter(
                name='branch',
                default='master'
            ),
            revision=FixedParameter(name='revision', default=''),
            repository=FixedParameter(name='repository', default=''),
            project=FixedParameter(name='project', default='')
        )
    ]

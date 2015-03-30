from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll
import projects
from projects import cmb
from projects.cmb.poll import REPO as CMB_REPO

__all__ = [
    'make_schedulers',
]

def make_schedulers(buildnames, secrets):
    # Setup defaults to use for all the codebases.
    # Note, this also acts as a change filter and hence must
    # include defaults for all relevant codebases.
    codebases = {}
    codebases.update(projects.get_codebase(project=cmb, secrets=secrets))
    codebases.update(projects.get_codebase(poll=poll, secrets=secrets))
    return [
        AnyBranchScheduler(
            name='CMBSuperbuild Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO,
                filter_fn=projects.get_change_filter_fn_for_buildbot_commands(accepted_values=['test', 'superbuild'])
            ),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='CMBSuperbuild \'merge-request\' created/changed.',
            properties={
                # For superbuilds, merge requests on superbuild itself should
                # always trigger a clean build, I suppose.
                'ctest_empty_binary_directory': True,
                'ctest_track': 'buildbot-packages',
            },
            codebases=codebases),
        AnyBranchScheduler(
            name='CMBSuperbuild Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='CMBSuperbuild \'master\' changed.',
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'master-packages',
            },
            codebases=codebases),
        AnyBranchScheduler(
            name='CMBSuperbuild CMB Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=CMB_REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='CMB \'master\' changed.',
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'master-packages',
            },
            codebases=codebases),
        AnyBranchScheduler(
            name='CMBSuperbuild CMB Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=CMB_REPO,
                # process those CMB MRs that have the command=superbuild.
                filter_fn=projects.get_change_filter_fn_for_buildbot_commands(accepted_values=['superbuild'])
            ),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='CMB \'merge-request\' created/changed with \'superbuild\' command',
            codebases=codebases,
            properties={
                'ctest_track': 'buildbot-packages',
            },
        ),
    ]

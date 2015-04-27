"""GeoJS test factory."""

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

import projects
from . import poll


def get_source_steps(sourcedir="source"):
    """Return a list of steps needed to checkout the source properly.

    @param sourcedir is the directory where to checkout the source.
    """
    update = Git(
        repourl=poll.REPO_SITE,
        mode='incremental',
        method='clean',
        submodules=True,
        workdir=sourcedir,
        reference=Property("referencedir"),
    )
    steps = []
    steps.append(update)
    steps.append(
        SetProperty(
            name="SetUVCDATSourceDir",
            property="sourcedir",
            value=sourcedir
        )
    )
    return steps


def get_factory(buildset):
    """Argument is the selected buildset.

    That could be used to build the factory as needed.
    """
    factory = BuildFactory()
    for step in get_source_steps():
        factory.addStep(step)

    factory.addStep(SetCTestBuildNameProperty())
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    if buildset["os"] == "windows":
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
        SetProperty(
            property="ctest_dashboard_script",
            value=Interpolate('%(prop:builddir)s/common.ctest')
        )
    )
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME))

    return factory

__all__ = [
    "get_factory",
    "get_source_steps"
]

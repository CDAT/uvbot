__all__ = [
    "get_factory",
    "get_source_steps"
]

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadCataystCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

import projects
from . import poll

def get_source_steps(sourcedir="source"):
    """Returns a list of steps needed to checkout VTK source properly.
    @param sourcedir is the directory where to checkout the source.
    """
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(repourl=poll.REPO_SITE + ':' + poll.REPO,
        mode='incremental',
        method='clean',
        submodules=False,
        workdir=sourcedir,
        reference=Property("referencedir"),
        codebase=codebase,
        env={'GIT_SSL_NO_VERIFY': 'true'})
    steps = []
    steps.append(update)
    steps.append(SetProperty(name="SetGeoJSSourceDir", property="sourcedir", value=sourcedir))
    return steps

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    codebase = projects.get_codebase_name(poll.REPO)
    factory = BuildFactory()
    for step in get_source_steps():
        factory.addStep(step)
    factory.addStep(SetCTestBuildNameProperty(codebases=[codebase]))
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    if buildset["os"] == "windows":
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
            SetProperty(property="ctest_dashboard_script",
                value=Interpolate('%(prop:builddir)s/common.ctest')))
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME))
    return factory

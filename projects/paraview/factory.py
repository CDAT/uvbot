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
                               makeUploadFetchSubmoduleScript,\
                               FetchUserSubmoduleForks,\
                               makeUploadTestSubmoduleScript,\
                               AreSubmodulesValid,\
                               SetGotRevision,\
                               SetCTestBuildNameProperty

import projects
from . import poll

def get_source_steps(sourcedir="source"):
    """Returns a list of steps needed to checkout ParaView source properly.
    @param sourcedir is the directory where to checkout the source.
    """
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(repourl=Interpolate("%(src:"+codebase+":repository)s"),
        mode='incremental',
        method='clean',
        submodules=True,
        workdir=sourcedir,
        reference=Property("referencedir"),
        haltOnFailure=False,
        flunkOnFailure=False,
        codebase=codebase,
        env={'GIT_SSL_NO_VERIFY': 'true'})

    steps = []
    steps.append(SetProperty(name="SetParaViewSourceDir", property="sourcedir", value=sourcedir))
    steps.append(update)
    steps.append(makeUploadFetchSubmoduleScript())
    steps.append(FetchUserSubmoduleForks())
    steps.append(SetGotRevision(codebase=codebase, workdir=sourcedir))
    return steps


def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""

    codebase = projects.get_codebase_name(poll.REPO)

    factory = BuildFactory()

    # add all source checkout steps.
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
    #factory.addStep(makeUploadTestSubmoduleScript())
    #factory.addStep(AreSubmodulesValid())
    return factory

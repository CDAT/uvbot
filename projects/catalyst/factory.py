__all__ = [
    "get_factory"
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
                               FetchTags

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    update = Git(name="update",
        repourl=Property("repository"),
        mode='incremental',
        submodules=True,
        workdir="source",
        reference=Property("referencedir"),
        haltOnFailure = False,
        env={'GIT_SSL_NO_VERIFY': 'true'})
    factory = BuildFactory()
    factory.addStep(update)
    factory.addStep(FetchTags())
    factory.addStep(makeUploadFetchSubmoduleScript())
    factory.addStep(FetchUserSubmoduleForks())
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(DownloadCataystCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    factory.addStep(
            SetProperty(property="ctest_dashboard_script",
                value=Interpolate('%(prop:builddir)s/catalyst.common.ctest')))
    factory.addStep(CTestDashboard())
    #factory.addStep(makeUploadTestSubmoduleScript())
    #factory.addStep(AreSubmodulesValid())
    return factory

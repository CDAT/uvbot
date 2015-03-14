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
                               CTestExtraOptionsDownload

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    update = Git(name="update",
        repourl=Property("repository"),
        mode='incremental',
        submodules=False,
        workdir="source",
        reference=Property("referencedir"),
        haltOnFailure = True,
        env={'GIT_SSL_NO_VERIFY': 'true'})
    factory = BuildFactory()
    factory.addStep(update)
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    if buildset["os"] == "windows":
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
            SetProperty(property="ctest_dashboard_script",
                value=Interpolate('%(prop:builddir)s/common.ctest')))
    factory.addStep(CTestDashboard())
    return factory

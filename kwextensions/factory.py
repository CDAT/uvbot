from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
import os

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

update = Git(name="update",
        repourl=Property("repository"),
        mode='incremental',
        submodules=True,
        workdir="source",
        reference=Property("referencedir"),
        haltOnFailure = False,
        env={'GIT_SSL_NO_VERIFY': 'true'})

mergeRequestBasicTestsFactory = BuildFactory()
mergeRequestBasicTestsFactory.addStep(update)
mergeRequestBasicTestsFactory.addStep(makeUploadFetchSubmoduleScript())
mergeRequestBasicTestsFactory.addStep(FetchUserSubmoduleForks())
mergeRequestBasicTestsFactory.addStep(DownloadCommonCTestScript())
mergeRequestBasicTestsFactory.addStep(CTestExtraOptionsDownload())
# DownloadLauncher is only needed for Windows.
mergeRequestBasicTestsFactory.addStep(DownloadLauncher())
mergeRequestBasicTestsFactory.addStep(
        SetProperty(property="ctest_dashboard_script",
            value=Interpolate('%(prop:builddir)s/common.ctest')))
mergeRequestBasicTestsFactory.addStep(CTestDashboard(
    timeout=60*60*2 # 2 hrs. Superbuilds can take a while without producing any output.
    ))
#mergeRequestBasicTestsFactory.addStep(makeUploadTestSubmoduleScript())
#mergeRequestBasicTestsFactory.addStep(AreSubmodulesValid())

def get_ctest_buildfactory():
    return mergeRequestBasicTestsFactory

catalystTestFactory = BuildFactory()
catalystTestFactory.addStep(update)
catalystTestFactory.addStep(FetchTags())
catalystTestFactory.addStep(makeUploadFetchSubmoduleScript())
catalystTestFactory.addStep(FetchUserSubmoduleForks())
catalystTestFactory.addStep(DownloadCommonCTestScript())
catalystTestFactory.addStep(DownloadCataystCTestScript())
catalystTestFactory.addStep(CTestExtraOptionsDownload())
catalystTestFactory.addStep(
        SetProperty(property="ctest_dashboard_script",
            value=Interpolate('%(prop:builddir)s/catalyst.common.ctest')))
catalystTestFactory.addStep(CTestDashboard())
#catalystTestFactory.addStep(makeUploadTestSubmoduleScript())
#catalystTestFactory.addStep(AreSubmodulesValid())

def get_catalyst_buildfactory():
    return catalystTestFactory

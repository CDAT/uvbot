from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.source.git import Git
from kwextensions.steps import CTestDashboard, CTestConfigDownload, CTestExtraOptionsDownload,\
                               CatalyzePreConfigure, CTestCatalystExtraOptionsDownload
import os

moduledir = os.path.dirname(os.path.abspath(__file__))

update = Git(name="update",
        repourl=Property("source_repo"), # FIXME: I think this can now change to "repository"
        mode='incremental',
        submodules=True,
        workdir="source",
        env={'GIT_SSL_NO_VERIFY': 'true'})

mergeRequestBasicTestsFactory = BuildFactory()
mergeRequestBasicTestsFactory.addStep(update)
mergeRequestBasicTestsFactory.addStep(CTestConfigDownload(mastersrc="%s/common.ctest" % moduledir))
mergeRequestBasicTestsFactory.addStep(CTestExtraOptionsDownload())
mergeRequestBasicTestsFactory.addStep(CTestDashboard())

def get_ctest_buildfactory():
    return mergeRequestBasicTestsFactory

catalyst_update = Git(name="update",
        repourl=Property("repository"),
        mode='incremental',
        submodules=True,
        workdir="source",
        env={'GIT_SSL_NO_VERIFY': 'true'})

catalystTestFactory = BuildFactory()
catalystTestFactory.addStep(catalyst_update)
catalystTestFactory.addStep(CatalyzePreConfigure())
catalystTestFactory.addStep(CTestConfigDownload(mastersrc="%s/catalyst.ctest" % moduledir))
catalystTestFactory.addStep(CTestCatalystExtraOptionsDownload())
catalystTestFactory.addStep(CTestDashboard())

def get_catalyst_buildfactory():
    return catalystTestFactory

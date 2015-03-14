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
                               FetchTags

from projects.paraview.factory import get_source_steps as get_paraview_source_steps

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    factory = BuildFactory()

    # add source steps to checkout paraview
    for step in get_paraview_source_steps():
        factory.addStep(step)
    factory.addStep(FetchTags())
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(DownloadCataystCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    factory.addStep(
            SetProperty(property="ctest_dashboard_script",
                value=Interpolate('%(prop:builddir)s/catalyst.common.ctest')))
    factory.addStep(CTestDashboard())
    return factory

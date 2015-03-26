__all__ = [
    "get_factory"
    "get_source_steps"
]

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
from buildbot.process import properties

from projects.vtk.factory import get_source_steps as get_vtk_source_steps
from projects.vtk import poll as vtk_poll

import projects
from . import poll

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

@properties.renderer
def _extra(props):
    extra_options = [
        ]
    return """
           """

def get_source_steps(sourcedir="source"):
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(repourl=Interpolate("%(src:"+codebase+":repository)s"),
        mode='incremental',
        method='clean',
        submodules=False,
        workdir=sourcedir,
        reference=Property("referencedir"),
        codebase=codebase,
        env={'GIT_SSL_NO_VERIFY': 'true'})

    steps = []
    steps.append(update)
    steps.append(SetProperty(name="SetSuperbuildSourceDir",
        property="sourcedir", value=sourcedir))
    return steps

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    factory = BuildFactory()

    codebases = [projects.get_codebase_name(poll.REPO)]

    # Add steps to checkout VtkSuperbuild codebase.
    for step in get_source_steps():
        factory.addStep(step)

    factory.addStep(SetCTestBuildNameProperty(codebases=codebases))
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload(
        s=Interpolate("%(kw:default)s%(kw:extra)s",
            default=CTestExtraOptionsDownload.DefaultRenderer,
            extra=_extra)))
    if buildset["os"] == "windows":
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
            SetProperty(property="ctest_dashboard_script",
                value=Interpolate('%(prop:builddir)s/common.ctest')))
    # We set a 2 hrs timeout since the vtk build step can take a while
    # without producing any output. When that happens, buildbot may kill the
    # process.
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME,
                                   timeout=60*60*2))
    return factory

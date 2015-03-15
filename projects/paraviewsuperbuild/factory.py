__all__ = [
    "get_factory"
    "get_source_steps"
]

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
from buildbot.process import properties

from projects.paraview.factory import get_source_steps as get_paraview_source_steps
from projects.paraview import poll as paraview_poll

import projects
from . import poll

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadCataystCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

@properties.renderer
def _extra(props):
    paraview_src_dir = "%s/source-paraview" % props.getProperty("builddir")
    paraview_src_dir = paraview_src_dir.replace("\\", "/")
    extra_options = [
        "-DParaView_FROM_GIT:BOOL=OFF",
        "-DParaView_FROM_SOURCE_DIR:BOOL=ON",
        "-DPARAVIEW_SOURCE_DIR:PATH=%s" % paraview_src_dir,
        ]
    return """
           # Extend the ctest_configure_options to pass options that set
           # the ParaView source dir for the Superbuild to use
           set (ctest_configure_options_extra "%s")
           set (ctest_configure_options "${ctest_configure_options};${ctest_configure_options_extra}")
           """ % ";".join(extra_options)

def get_source_steps(sourcedir="source"):
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(repourl=Interpolate("%(src:"+codebase+":repository)s"),
        mode='incremental',
        submodules=False,
        workdir=sourcedir,
        reference=Property("referencedir"),
        haltOnFailure = True,
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

    codebases = [projects.get_codebase_name(poll.REPO),
                 projects.get_codebase_name(paraview_poll.REPO)]

    # Add steps to checkout ParaView codebase.
    for step in get_paraview_source_steps(sourcedir="source-paraview"):
        factory.addStep(step)

    # Add steps to checkout ParaViewSuperbuild codebase.
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
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME))
    return factory

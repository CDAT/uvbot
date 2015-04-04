__all__ = [
    "get_factory",
    "get_source_steps"
]

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate, renderer
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
    steps.append(update)
    steps.append(SetProperty(name="SetParaViewSourceDir", property="sourcedir", value=sourcedir))
    steps.append(makeUploadFetchSubmoduleScript())
    steps.append(FetchUserSubmoduleForks())
    steps.append(SetGotRevision(codebase=codebase, workdir=sourcedir))
    return steps

MaxFailedTestCount = 15

def _doStepIf(step):
    global MaxFailedTestCount
    ctest_failed_tests = step.getProperty("ctest_failed_tests", [])
    return len(ctest_failed_tests) > 0 and len(ctest_failed_tests) < MaxFailedTestCount

@renderer
def _convertTestsToRegEx(props):
    """Converts a list of test names to a list of regex matching the test names"""
    ctest_failed_tests = props.getProperty("ctest_failed_tests", [])
    return ["^%s$" % x for x in ctest_failed_tests]

def get_factory(buildset):
    """Argument is the selected buildset. That could be used to build the
    factory as needed."""
    global MaxFailedTestCount

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
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME,
        maxFailedTestCount=MaxFailedTestCount))

    retrycount = 1
    if retrycount:
        # Ensure we don't empty the binary directory.
        factory.addStep(SetProperty(property="ctest_empty_binary_directory", value=False))
        # This time, force serial tests.
        factory.addStep(SetProperty(property="supports_parallel_testing", value=False))
        # Do only testing (skip configure & build)
        factory.addStep(SetProperty(property="ctest_stages", value="test"))

    for i in range(retrycount):
        # Convert the "ctest_failed_tests" property to "ctest_test_includes".
        factory.addStep(SetProperty(property="test_includes",
            value=_convertTestsToRegEx,
            doStepIf=_doStepIf))
        # Download the new ctest_extra_options.cmake file.
        factory.addStep(CTestExtraOptionsDownload(doStepIf=_doStepIf))
        # Rerun the dashboard for the failed tests.
        maxFailedTestCount = MaxFailedTestCount if i < (retrycount-1) else 0
        factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME,
            maxFailedTestCount=maxFailedTestCount,
            doStepIf=_doStepIf))
    return factory

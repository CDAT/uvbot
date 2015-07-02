"""GeoJS test factory."""

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate, renderer
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

from . import poll


class ACMETest(CTestDashboard):

    """Run configuration and build."""

    def __init__(self, cdash_projectname, stages, source=None):
        """Initialize the class."""
        self.warnCount = 0
        self.errorCount = 0
        self.failedTestsCount = 0
        self.maxFailedTestCount = 0
        self.cdash_projectname = cdash_projectname
        self.stages = stages
        if self.stages is 'test':
            keep = 'ON'
        else:
            keep = 'OFF'
        if source is None:
            self.source = ''
        else:
            self.source = source

        @renderer
        def command(props):
            """Generate the ctest commandline."""
            props_dict = {'prop:ctest_stages': self.stages}

            for (key, (value, source)) in props.asDict().iteritems():
                props_dict["prop:%s" % key] = value

            return '/bin/bash -c \'' + (self.source + ' '.join([
                '"%(prop:cmakeroot)s/bin/ctest"',
                '-V',
                '"-Dctest_extra_options_file:STRING'
                '=%(prop:builddir)s/ctest_extra_options.cmake"',
                '"-Dctest_stages:STRING=%(prop:ctest_stages)s"',
                '"-Dctest_keep_build=' + keep + '"',
                '-C',
                '"' + props.getProperty('configure_options')[
                    'CMAKE_BUILD_TYPE:STRING'
                ] + '"',
                '-S',
                '"%(prop:ctest_dashboard_script)s"'
            ])) % props_dict + '\''

        ShellCommand.__init__(
            self,
            command=command
        )


def get_source_steps(sourcedir="source"):
    """Return a list of steps needed to checkout the source properly.

    @param sourcedir is the directory where to checkout the source.
    """
    update = Git(
        repourl=poll.REPO_SITE,
        mode='incremental',
        method='clean',
        submodules=True,
        workdir=sourcedir,
        reference=Property("referencedir"),
    )
    steps = []
    steps.append(update)
    steps.append(
        SetProperty(
            name="SetUVCDATSourceDir",
            property="sourcedir",
            value=sourcedir
        )
    )
    return steps


def get_factory(buildset):
    """Argument is the selected buildset.

    That could be used to build the factory as needed.
    """
    factory = BuildFactory()
    for step in get_source_steps():
        factory.addStep(step)

    factory.addStep(SetCTestBuildNameProperty())
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload())
    if buildset["os"] == "windows":
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
        SetProperty(
            property="ctest_dashboard_script",
            value=Interpolate('%(prop:builddir)s/common.ctest')
        )
    )
    factory.addStep(
        CTestDashboard(
            cdash_projectname=poll.CDASH_PROJECTNAME,
        )
    )

    return factory

__all__ = [
    "get_factory",
    "get_source_steps"
]

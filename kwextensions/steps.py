from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.steps.shell import ShellCommand, WarningCountingShellCommand
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload

from buildbot.status.results import FAILURE
from buildbot.status.results import SUCCESS
from buildbot.status.results import WARNINGS

from twisted.python import log as twisted_log

import re
class GitWithSubmodules(Git):
    """
    Extends buildbot's Git to fetch submodule objects
    from forked repos.

    Grrr...this is harder!  Let's just assume for now that one's submodule
    changes needs to be merged upstream before the dependent projects can be
    tested :(.
    """
    def __init__(self, submodules=False, **kwargs):
        self.handleSubmodules = submodules
        # Don't let superclass handle the submodules since it can't do it well.
        # We'll handle it here.
        Git.__init__(self, submodules=False, **kwargs)


class CTestDashboard(ShellCommand):
    name="build-n-test"
    description="building-n-testing"
    descriptionDone="built and tested"
    def __init__(self, model="Experimental", command=None, properties={}, **kwargs):
        self.warnCount = 0
        self.errorCount = 0

        ShellCommand.__init__(self,
                command=[
                    Interpolate('%(prop:cmakeroot)s/bin/ctest'),
                    '-VV',
                    '-D',
                    Interpolate('ctest_command:STRING=%(prop:workdir)s/bin/ctest'),
                    '-D',
                    Interpolate('ctest_source:STRING=%(prop:workdir)s/source'),
                    '-D',
                    Interpolate('ctest_build:STRING=%(prop:workdir)s/build'),
                    '-D',
                    'ctest_model:STRING=%s' % model,
                    '-D',
                    Interpolate('ctest_generator:STRING=%(prop:generator)s'),
                    '-D',
                    Interpolate('ctest_buildname:STRING=%(prop:source_branch)s-%(prop:buildername)s'),
                    '-D',
                    Interpolate('ctest_site:STRING=%(prop:slavename)s'),
                    '-D',
                    Interpolate('ctest_configure_options_file:STRING=%(prop:workdir)s/ctest_configure_options.cmake'),
                    '-D',
                    Interpolate('ctest_test_excludes_file:STRING=%(prop:workdir)s/ctest_test_excludes.cmake'),
                    '-D',
                    Interpolate('ctest_stages:STRING=%(prop:ctest_stages:-all)s'),
                    '-S',
                    Interpolate('%(prop:workdir)s/common.ctest')],
                **kwargs)

    def createSummary(self, log):
        """
        Generate summary for this build. We use special output from CTest and
        our common.cmake file to provide improved summary.
        """
        self.warnCount = 0
        self.errorCount = 0
        self.failedTestsCount = 0
        self.totalTestsCount = 0
        self.testSuccessRate = 0

        read_build_summary = False
        read_test_summary = False
        summaryRe = re.compile(r"BUILDBOT BUILD SUMMARY: (\d+)/(\d+)")
        testRe = re.compile(r"(\d+)% tests passed, (\d+) tests failed out of (\d)+")
        failedTestsListRe = re.compile(r"The following tests FAILED:")

        failedTestsHeader = []
        failedTests = []

        for line in log.readlines():
            if not read_build_summary:
                g = summaryRe.match(line)
                if g:
                    self.warnCount = int(g.group(1))
                    self.errorCount = int(g.group(2))
                    read_build_summary = True
                    continue
            if not read_test_summary:
                g = testRe.match(line)
                if g:
                    self.testSuccessRate = int(g.group(1))
                    self.failedTestsCount = int(g.group(2))
                    self.totalTestsCount = int(g.group(3))
                    read_test_summary = True
                    failedTestsHeader.append(line.strip())
                    continue
            if read_test_summary and failedTestsListRe.match(line):
                failedTestsHeader.append(line.strip())
                continue
            if len(failedTestsHeader) == 2 and len(failedTests) < self.failedTestsCount:
                failedTests.append(line.strip())
                continue

        if self.warnCount:
            self.addCompleteLog("warnings (%d)" % self.warnCount, "--coming soon--")
        if self.errorCount:
            self.addCompleteLog("error (%d)" % self.errorCount, "--coming soon--")
        if self.failedTestsCount:
            # TODO: I can make this produce an HTML page that lists tests with links to CDash.
            failedTests = failedTestsHeader + failedTests
            self.addCompleteLog('%d failed tests' % self.failedTestsCount,
                    "\n".join(failedTests) + "\n")

    def evaluateCommand(self, cmd):
        """return command state"""
        result = ShellCommand.evaluateCommand(self, cmd)
        if result != SUCCESS:
            return result
        if self.errorCount or self.failedTestsCount:
            return FAILURE
        if self.warnCount:
            return WARNINGS
        return SUCCESS


class CTestConfigDownload(FileDownload):
    """Step to send the common.cmake file to the slave before each dashboard run."""
    def __init__(self, mastersrc, slavedest=None, **kwargs):
        FileDownload.__init__(self, mastersrc=mastersrc,
                slavedest=Interpolate("%(prop:workdir)s/common.ctest"),
                **kwargs)


def _get_config_contents(prefix, patternstr, joinstr):
    @properties.renderer
    def makeCommand(props):
        # if there's a cmake-configure-args property, pass those to
        # ctest_configure_options.
        lines = []
        regex = re.compile("^%s:(.*)$" % prefix)
        for (key, (value, source)) in props.asDict().iteritems():
            m = regex.match(key)
            if m and m.group(1):
                lines.append(patternstr % (m.group(1), str(value)))
        return joinstr.join(lines)
    return makeCommand


class CTestConfigureOptionsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=_get_config_contents(prefix='cc', patternstr='-D%s=%s', joinstr=';'),
                slavedest=Interpolate("%(prop:workdir)s/ctest_configure_options.cmake"),
                **kwargs)

@properties.renderer
def _get_test_excludes(props):
    excludes = []
    regex = re.compile('^test_excludes:.*$')
    for (key, (value, source)) in props.asDict().iteritems():
        if regex.match(key):
            excludes += value
    return "|".join(excludes)

class CTestTestArgsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=_get_test_excludes,
                slavedest=Interpolate("%(prop:workdir)s/ctest_test_excludes.cmake"),
                **kwargs)

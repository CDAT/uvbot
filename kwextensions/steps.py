from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.steps.shell import ShellCommand, WarningCountingShellCommand
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload

from buildbot.status.results import FAILURE
from buildbot.status.results import SUCCESS
from buildbot.status.results import WARNINGS

from twisted.python import log as twisted_log
from urllib import urlencode
from datetime import datetime, timedelta

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
        # TODO: we maybe can convert all these arguments to be passed in through
        # the ctest_extra_options file.
        ShellCommand.__init__(self,
                command=[
                    Interpolate('%(prop:cmakeroot)s/bin/ctest'),
                    '-V',
                    '-D',
                    Interpolate('ctest_command:STRING=%(prop:cmakeroot)s/bin/ctest'),
                    '-D',
                    Interpolate('ctest_source:STRING=%(prop:builddir)s/source'),
                    '-D',
                    Interpolate('ctest_build:STRING=%(prop:builddir)s/build'),
                    '-D',
                    'ctest_model:STRING=%s' % model,
                    '-D',
                    Interpolate('ctest_generator:STRING=%(prop:generator)s'),
                    '-D',
                    # we're creating an unique buildname per build.
                    # that makes it possible to link back to Cdash summary page easily.
                    Interpolate('ctest_buildname:STRING=build%(prop:buildnumber)s-%(prop:buildername)s'),
                    '-D',
                    Interpolate('ctest_site:STRING=%(prop:slavename)s'),
                    '-D',
                    Interpolate('ctest_extra_options_file:STRING=%(prop:builddir)s/ctest_extra_options.cmake'),
                    '-D',
                    Interpolate('ctest_stages:STRING=%(prop:ctest_stages:-all)s'),
                    '-S',
                    Interpolate('%(prop:builddir)s/common.ctest')],
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

        read_warning_summary = False
        read_error_summary = False
        read_test_summary = False
        errorsRe = re.compile(r"\s*(\d+) Compiler errors")
        warningsRe = re.compile(r"\s*(\d+) Compiler warnings")
        testRe = re.compile(r"(\d+)% tests passed, (\d+) tests failed out of (\d)+")

        for line in log.readlines():
            if not read_warning_summary:
                g = warningsRe.match(line.strip())
                if g:
                    self.warnCount = int(g.group(1))
                    read_warning_summary = True
                    continue
            if not read_error_summary:
                g = errorsRe.match(line.strip())
                if g:
                    self.errorCount = int(g.group(1))
                    read_error_summary = True
                    continue
            if not read_test_summary:
                g = testRe.match(line)
                if g:
                    self.testSuccessRate = int(g.group(1))
                    self.failedTestsCount = int(g.group(2))
                    self.totalTestsCount = int(g.group(3))
                    read_test_summary = True
                    continue
            if read_warning_summary and read_error_summary and read_test_summary:
                break

        buildnumber = self.getProperty("buildnumber")
        buildername = self.getProperty("buildername")
        buildid = "build%s-%s" % (buildnumber, buildername)
        project = self.getProperty("project")
        cdash_root = self.getProperty("cdash_url")
        cdash_projectname = self.getProperty("cdash_project_names")[project]

        cdash_index_url = cdash_root + "/index.php"
        cdash_test_url = cdash_root + "/queryTests.php"

        common_query = {}
        common_query["project"] = cdash_projectname
        common_query["showfilters"] = 0
        common_query["limit"] = 100
        common_query["showfeed"] = 0

        build_dashboard_query = {}
        build_dashboard_query.update(common_query)
        build_dashboard_query["filtercount"] = 2
        build_dashboard_query["field1"] = "buildname/string"
        build_dashboard_query["compare1"] = 61
        build_dashboard_query["value1"] = buildid
        build_dashboard_query["field2"] = "buildstarttime/date"
        build_dashboard_query["compare2"] = 83
        # pick yesterday, justo be safe.
        build_dashboard_query["value2"] = \
                (datetime.now() + timedelta(days=-1)).strftime("%Y%m%d")

        if self.warnCount:
            self.addURL("warnings (%d)" % self.warnCount,
                    cdash_index_url + "?" + urlencode(build_dashboard_query))
        if self.errorCount:
            self.addURL("error (%d)" % self.errorCount,
                    cdash_index_url + "?" + urlencode(build_dashboard_query))
        if self.failedTestsCount:
            test_query = {}
            test_query.update(build_dashboard_query)
            test_query["filtercount"] = 3
            test_query["filtercombine"] = "and"
            test_query["field3"] = "status/string"
            test_query["compare3"] = "61"
            test_query["value3"] = "Failed"
            self.addURL('%d failed tests' % self.failedTestsCount,
                    cdash_test_url + "?" + urlencode(test_query))
        if not self.warnCount and not self.errorCount:
            # put the direct dashboard link if not already placed.
            self.addURL("cdash", cdash_index_url + "?" + urlencode(build_dashboard_query))

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
                slavedest=Interpolate("%(prop:builddir)s/common.ctest"),
                **kwargs)

def _get_test_params(props, prefix, joinstr):
    excludes = []
    regex = re.compile('^%s:.*$' % prefix)
    for (key, (value, source)) in props.asDict().iteritems():
        if regex.match(key):
            excludes += value
    return joinstr.join(excludes)

def _get_configure_options(props):
    source_precedence = ["BuildSlave", "Builder", "Build"]
    regex = re.compile('^configure_options:.*$')

    option_dicts = {}
    for (key, (value, source)) in props.asDict().iteritems():
        if not regex.match(key): continue
        if type(value) != dict:
            raise RuntimeError('%s: value must be a dict!' % key)
        try:
            index = source_precedence.index(source)
            option_dicts[index] = value
        except IndexError:
            raise RuntimeError('%s: source (%s) unrecognized!' % (key, source))

    config = {}
    for option in option_dicts.values():
        config.update(option)
    lines = [ "-D%s=%s" % (key, str(value)) for key, value in config.iteritems() ]
    return ";".join(lines)

@properties.renderer
def makeExtraOptionsString(props):
    return """
            # Extra configuration options for this build.
            # Options to pass to the configure stage.
            set (ctest_configure_options "%s")

            # Test excludes
            set (ctest_test_excludes "%s")

            # Test include labels
            set (ctest_test_include_labels "%s")

            set (ctest_upload_file_patterns "%s")

            """ % (_get_configure_options(props),
                   _get_test_params(props, "test_excludes", "|"),
                   _get_test_params(props, "test_include_labels", "|"),
                   _get_test_params(props, "upload_file_patterns", ";")
                   )

class CTestExtraOptionsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=makeExtraOptionsString,
                slavedest=Interpolate("%(prop:builddir)s/ctest_extra_options.cmake"),
                **kwargs)

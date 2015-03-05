from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.process.buildstep import LogLineObserver
from buildbot.steps.shell import ShellCommand, WarningCountingShellCommand
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload

from buildbot.status.results import FAILURE, SUCCESS, WARNINGS
from twisted.python import log as twisted_log
from urllib import urlencode
from datetime import datetime, timedelta

Gitlab_Base_URL = "https://kwgitlab.kitwarein.com"

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

@properties.renderer
def makeCTestDashboardCommand(props):
    props_dict = {'prop:ctest_stages' : 'all'}
    for (key, (value, source)) in props.asDict().iteritems():
        props_dict["prop:%s" % key] = value
    command = ['%(prop:cmakeroot)s/bin/ctest' % props_dict,
            '-VV',
            '-Dctest_extra_options_file:STRING=%(prop:builddir)s/ctest_extra_options.cmake' % props_dict,
            '-Dctest_stages:STRING=%(prop:ctest_stages)s' % props_dict,
            '-S',
            '%(prop:ctest_dashboard_script)s' % props_dict
            ]
    if not props.getProperty('vcvarsall'):
        return command
    command_prefix = ["call",
            "%(prop:builddir)s/vclauncher.bat" % props_dict
            ]
    command_prefix.extend(command)
    return command_prefix

# Generates the command to fetch the user's fork of submodules
@properties.renderer
def makeUserForkCommand(props):
    repo = props.getProperty('repository')
    cmd = ''
    if props.hasProperty('username') and props.hasProperty('try_user_fork') and\
            props.getProperty('try_user_fork') == True:
        argList = ['git', 'submodule', 'foreach', 'cmake']
        username = props.getProperty('username')
        basedir = props.getProperty('builddir')
        cmakefile = '%s/fetch_submodule.cmake' % basedir
        argList.append('-Dusername:STRING=%s' % username)
        argList.append('-Durl_prefix:STRING=%s' % Gitlab_Base_URL)
        argList += ['-P', cmakefile]
        cmd = " ".join(argList) + ' && git submodule update --init'
    return cmd

def failureForSubmodule(step):
    from buildbot.status.builder import FAILURE
    lastStep = step.build.getStatus().getSteps()[0]
    output = lastStep.getLogs()[0].getText()
    return step.build.result == FAILURE and output.find('in submodule path') != -1

def makeUploadFetchSubmoduleScript(**kwargs):
    import os
    moduledir = os.path.dirname(os.path.abspath(__file__))
    step = FileDownload(mastersrc="%s/fetch_submodule.cmake" % moduledir,
                        slavedest=Interpolate("%(prop:builddir)s/fetch_submodule.cmake"),
                        haltOnFailure=True,
                        doStepIf=failureForSubmodule,
                        **kwargs)
    return step

class FetchUserSubmoduleForks(ShellCommand):
    def __init__(self, **kwargs):
        ShellCommand.__init__(self,command=makeUserForkCommand,
                              haltOnFailure=True,
                              flunkOnFailure=True,
                              doStepIf=failureForSubmodule,
                              workdir=Interpolate('%(prop:builddir)s/source'),
                              description=["Trying user's submodule forks..."],
                              descriptionDone=["Tried user's submodule forks"],
                              env={'GIT_SSL_NO_VERIFY': 'true'},
                              **kwargs)

def makeUploadTestSubmoduleScript(**kwargs):
    import os
    moduledir = os.path.dirname(os.path.abspath(__file__))
    step = FileDownload(mastersrc="%s/test_submodule.cmake" % moduledir,
                        slavedest=Interpolate("%(prop:builddir)s/test_submodule.cmake"),
                        haltOnFailure=True,
                        **kwargs)
    return step

@properties.renderer
def makeSubmoduleTestCommand(props):
    cmd = ['git', 'submodule', 'foreach', 'cmake', '-P']
    builddir = props.getProperty('builddir')
    cmd.append('%s/test_submodule.cmake' % builddir)
    return cmd


class AreSubmodulesValid(ShellCommand):
    def __init__(self, **kwargs):
        ShellCommand.__init__(self,command = makeSubmoduleTestCommand,
                              warnOnFailure=True,
                              workdir=Interpolate('%(prop:builddir)s/source'),
                              description=['Testing if submodules are merged'],
                              descriptionDone=['Are submodules merged'],
                              **kwargs)

class CTestDashboard(ShellCommand):
    name="build-n-test"
    description="building-n-testing"
    descriptionDone="built and tested"
    def __init__(self, command=None, **kwargs):
        self.warnCount = 0
        self.errorCount = 0
        # TODO: we maybe can convert all these arguments to be passed in through
        # the ctest_extra_options file.
        ShellCommand.__init__(self,
                command=makeCTestDashboardCommand,
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
        shortrevision = self.getProperty('got_revision')[0:8]
        buildid = "%s-build%s-%s" % (shortrevision, buildnumber, buildername)
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
    props_dict = {'prop:model' : 'Experimental'}
    for (key, (value, source)) in props.asDict().iteritems():
        if isinstance(value, str):
            value = value.replace("\\", '/')
        props_dict["prop:%s" % key] = value
    props_dict['ctest_configure_options'] = _get_configure_options(props)
    props_dict['ctest_test_excludes'] = _get_test_params(props, "test_excludes", "|")
    props_dict['ctest_test_include_labels'] = _get_test_params(props, "test_include_labels", "|")
    props_dict['ctest_upload_file_patterns'] = _get_test_params(props, "upload_file_patterns", ";")
    props_dict['shortrevision'] = props.getProperty('got_revision')[0:8]
    return """
            # Essential options.
            set (CTEST_COMMAND "%(prop:cmakeroot)s/bin/ctest")
            set (CTEST_SOURCE_DIRECTORY "%(prop:builddir)s/source")
            set (CTEST_BINARY_DIRECTORY "%(prop:builddir)s/build")
            set (CTEST_CMAKE_GENERATOR "%(prop:generator)s")

            # we're creating an unique buildname per build.
            # that makes it possible to link back to Cdash summary page easily.
            set (CTEST_BUILD_NAME "%(shortrevision)s-build%(prop:buildnumber)s-%(prop:buildername)s")
            set (CTEST_SITE "%(prop:slavename)s")

            set (CTEST_BUILD_FLAGS "%(prop:buildflags)s")

            # Extra configuration options for this build.
            set (ctest_model "%(prop:model)s")

            # Options to pass to the configure stage.
            set (ctest_configure_options "%(ctest_configure_options)s")

            # Test excludes
            set (ctest_test_excludes "%(ctest_test_excludes)s")

            # Test include labels
            set (ctest_test_include_labels "%(ctest_test_include_labels)s")

            set (ctest_upload_file_patterns "%(ctest_upload_file_patterns)s")
            """ % props_dict

class CTestExtraOptionsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=makeExtraOptionsString,
                slavedest=Interpolate("%(prop:builddir)s/ctest_extra_options.cmake"),
                **kwargs)

class DownloadLauncher(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        global _vclauncher
        StringDownload.__init__(self,
                s=Interpolate("""rem Name: vclauncher.bat
rem Task: launch ctest after setting appropriate environment for Visual Studio compilers.
@echo on
call "%(prop:vcvarsall)s" %(prop:vcvarsargument)s
call %%*
"""),
                slavedest=Interpolate("%(prop:builddir)s/vclauncher.bat"),
                **kwargs)

import os
moduledir = os.path.dirname(os.path.abspath(__file__))

class DownloadCommonCTestScript(FileDownload):
    def __init__(self, mastersrc=None, slavedest=None, **kwargs):
        global moduledir
        FileDownload.__init__(self,
                mastersrc= "%s/common.ctest" % moduledir,
                slavedest=Interpolate("%(prop:builddir)s/common.ctest"),
                **kwargs)

class DownloadCataystCTestScript(FileDownload):
    def __init__(self, mastersrc=None, slavedest=None, **kwargs):
        global moduledir
        FileDownload.__init__(self,
                mastersrc= "%s/catalyst.common.ctest" % moduledir,
                slavedest=Interpolate("%(prop:builddir)s/catalyst.common.ctest"),
                **kwargs)

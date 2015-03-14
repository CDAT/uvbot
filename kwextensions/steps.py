from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.process.buildstep import LogLineObserver
from buildbot.steps.shell import ShellCommand, WarningCountingShellCommand
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload

from buildbot.status.results import FAILURE, SUCCESS, WARNINGS
from twisted.python import log as twisted_log
from datetime import datetime, timedelta
import cdash

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

def makeUserForkCommandWrapper(codebase):
    # TODO: I'm sure I need to use the codebase to determine the
    # repository...just don't know how yet :/
    # Generates the command to fetch the user's fork of submodules
    @properties.renderer
    def makeUserForkCommand(props):
        repo = props.getProperty('repository')
        cmd = []
        if props.hasProperty('owner') and props.hasProperty('try_user_fork') and\
                props.getProperty('try_user_fork') == True:
            argList = ['git', 'submodule', 'foreach',]
            cmakeRoot = props.getProperty('cmakeroot')
            username = props.getProperty('owner')
            basedir = props.getProperty('builddir').replace('\\', '/')
            cmakefile = '%s/fetch_submodule.cmake' % basedir
            argList += ['%s/bin/cmake' % cmakeRoot, '-Dusername:STRING=%s' % username,]
            argList.append('-Durl_prefix:STRING=%s' % Gitlab_Base_URL)
            argList += ['-P', cmakefile]
            cmd = argList + ['&&', 'git', 'submodule', 'update', '--init']
            # Copy into got_revision since Update failed
            props.setProperty('got_revision', props.getProperty('revision'), 'UserFork')
        return ' '.join(cmd)
    return makeUserForkCommand

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

class FetchTags(ShellCommand):
    def __init__(self, **kwargs):
        ShellCommand.__init__(self,command=['git', 'fetch', '--tags', Interpolate('%(prop:upstream_repo)s')],
                              haltOnFailure=True,
                              flunkOnFailure=True,
                              workdir=Interpolate('%(prop:builddir)s/%(prop:sourcedir:-source)s'),
                              description=["Fetching tags"],
                              descriptionDone=["Fetched tags"],
                              env={'GIT_SSL_NO_VERIFY': 'true'},
                              **kwargs)

class FetchUserSubmoduleForks(ShellCommand):
    def __init__(self, codebase='', **kwargs):
        ShellCommand.__init__(self, command=makeUserForkCommandWrapper(codebase),
                              haltOnFailure=True,
                              flunkOnFailure=True,
                              doStepIf=failureForSubmodule,
                              workdir=Interpolate('%(prop:builddir)s/%(prop:sourcedir:-source)s'),
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
                        alwaysRun=True,
                        **kwargs)
    return step

@properties.renderer
def makeSubmoduleTestCommand(props):
    cmd = ['git', 'submodule', 'foreach',]
    cmakeRoot = props.getProperty('cmakeroot')
    builddir = props.getProperty('builddir')
    cmd += ['%s/bin/cmake' % cmakeRoot, '-P',]
    cmd.append('%s/test_submodule.cmake' % builddir)
    return cmd


class TestScriptOutputLogger(LogLineObserver):
    inMaster = {} # hash of submodule name to bool
    firstParentOfMaster = {} # hash of submodule name to bool
    allInMaster = True
    allFirstParentOfMaster = True
    currentSubmodule = ''
    def lineReceived(self, line, lineType):
        if line.find('Entering') == 0:
            self.currentSubmodule = line[9:]
            self.inMaster[self.currentSubmodule] = True
            self.firstParentOfMaster[self.currentSubmodule] = True
        elif line.find('Error: commits are not merged to master.') != -1:
            self.allInMaster = False
            self.inMaster[self.currentSubmodule] = False
        elif line.find('Error: head is not in the first parent list of master.') != -1:
            self.allFirstParentOfMaster = False
            self.firstParentOfMaster[self.currentSubmodule] = False
    def outLineReceived(self,line):
        self.lineReceived(line,'out')
    def errLineReceived(self,line):
        self.lineReceived(line,'err')

class AreSubmodulesValid(ShellCommand):
    def __init__(self, **kwargs):
        self.myLogger = TestScriptOutputLogger()
        ShellCommand.__init__(self,command = makeSubmoduleTestCommand,
                              alwaysRun=True,
                              workdir=Interpolate('%(prop:builddir)s/%(prop:sourcedir:-source)s'),
                              description=['Testing if submodules are merged'],
                              descriptionDone=['Are submodules merged'],
                              **kwargs)
        self.addLogObserver('stdio',self.myLogger)
        self.addLogObserver('stderr',self.myLogger)
    def evaluateCommand(self, cmd):
        """return command state"""
        result = ShellCommand.evaluateCommand(self, cmd)
        if result != SUCCESS:
            return result
        elif self.myLogger.allFirstParentOfMaster:
            return SUCCESS
        elif self.myLogger.allInMaster:
            return WARNINGS # TODO should this succeed?
        else: # TODO - error messages?  I collected info in the logger...
            return WARNINGS

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
        cdash_projectname = self.getProperty("cdash_projectnames")[project]

        cdash_index_url = cdash_root + "/index.php"
        cdash_test_url = cdash_root + "/queryTests.php"

        query = cdash.Query(project=cdash_projectname)
        query.add_filter(("buildname/string", cdash.StringOp.STARTS_WITH, buildid))
        query.add_filter(("buildstarttime/date", cdash.DateOp.IS_AFTER, self.getProperty('cdash_time')))

        # add a link to summary on cdash.
        self.addURL("cdash", query.get_url(cdash_index_url))

        if self.warnCount:
            self.addURL("warnings (%d)" % self.warnCount, query.get_url(cdash_index_url))
        if self.errorCount:
            self.addURL("error (%d)" % self.errorCount, query.get_url(cdash_index_url))
        if self.failedTestsCount:
            query.add_filter(("status/string", cdash.StringOp.IS, "Failed"))
            self.addURL('%d failed tests' % self.failedTestsCount,
                    query.get_url(cdash_test_url))

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
    props_dict = {
        'prop:model' : 'Experimental',
        'prop:ctest_empty_binary_directory': False,
        'prop:sourcedir' : "source",
        }
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
            set (CTEST_SOURCE_DIRECTORY "%(prop:builddir)s/%(prop:sourcedir)s")
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

            set (ctest_use_empty_binary_directory "%(prop:ctest_empty_binary_directory)s")
            """ % props_dict

class CTestExtraOptionsDownload(StringDownload):
    DefaultRenderer = makeExtraOptionsString

    def __init__(self, s=makeExtraOptionsString, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=s,
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

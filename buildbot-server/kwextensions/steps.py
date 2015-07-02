from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.process.buildstep import LogLineObserver
from buildbot.steps.shell import ShellCommand, WarningCountingShellCommand, SetPropertyFromCommand
from buildbot.steps.master import SetProperty
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload
from zope.interface import implements

from buildbot.status.results import FAILURE, SUCCESS, WARNINGS
from twisted.python import log as twisted_log
from datetime import datetime, timedelta
import cdash

Gitlab_Base_URL = "https://gitlab.kitware.com"

import re


@properties.renderer
def makeCTestDashboardCommand(props):
    props_dict = {'prop:ctest_stages' : 'all'}
    for (key, (value, source)) in props.asDict().iteritems():
        props_dict["prop:%s" % key] = value
    verbose = '-V'
    if props_dict.get('prop:dashboard_status', None) == 'experimental':
        verbose = '-VV'
    command = ['%(prop:cmakeroot)s/bin/ctest' % props_dict,
            verbose,
            '-Dctest_extra_options_file:STRING=%(prop:builddir)s/ctest_extra_options.cmake' % props_dict,
            '-Dctest_stages:STRING=%(prop:ctest_stages)s' % props_dict,
            '-C', props.getProperty('configure_options')['CMAKE_BUILD_TYPE:STRING'], # FIXME: this is bad
            '-S',
            '%(prop:ctest_dashboard_script)s' % props_dict
            ]
    if not props.getProperty('vcvarsall'):
        return command
    command_prefix = ["call",
        "%(prop:builddir)s/vclauncher.bat" % props_dict,
    ]
    command_prefix.extend(command)
    return command_prefix

# Generates the command to fetch the user's fork of submodules
@properties.renderer
def makeUserForkCommand(props):
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
    return ' '.join(cmd)

def failureForSubmodule(step):
    from buildbot.status.builder import FAILURE
    lastStep = step.build.getStatus().getSteps()[0]
    output = lastStep.getLogs()[0].getText()
    hasMsg1 = output.find('Unable to checkout') != -1 and output.find('in submodule path') != -1
    hasMsg2 = output.find('Unable to find current revision in submodule path') != -1
    return hasMsg1 or hasMsg2

class SubmoduleForkLogObserver(LogLineObserver):
    def __init__(self, **kwargs):
        LogLineObserver.__init__(self, **kwargs)
        self.success = True

    def lineReceived(self, line, lineType):
        if line.find('Unable to checkout') != -1 and line.find('in submodule path') != -1:
            self.success = False
        if line.find('Unable to find current revision in submodule path') != -1:
            self.success = False
    def outLineReceived(self,line):
        self.lineReceived(line,'out')
    def errLineReceived(self,line):
        self.lineReceived(line,'err')


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
    def __init__(self, **kwargs):
        self.logObserver = SubmoduleForkLogObserver()
        ShellCommand.__init__(self,command=makeUserForkCommand,
                              haltOnFailure=True,
                              flunkOnFailure=True,
                              doStepIf=failureForSubmodule,
                              workdir=Interpolate('%(prop:builddir)s/%(prop:sourcedir:-source)s'),
                              description=["Trying user's submodule forks..."],
                              descriptionDone=["Tried user's submodule forks"],
                              env={'GIT_SSL_NO_VERIFY': 'true'},
                              **kwargs)
        self.addLogObserver('stdio',self.logObserver)
        self.addLogObserver('stderr',self.logObserver)
    def evaluateCommand(self, cmd):
        """return command state"""
        result = ShellCommand.evaluateCommand(self, cmd)
        if not self.logObserver.success:
            return FAILURE
        else:
            return result

class SetGotRevision(SetPropertyFromCommand):
    """Command used to setup got-revision. This is needed since the Source step
    may fail to setup got_revision when dealing with submodules.
    This step is needed any time you have a Source step that doesn't
    haltOnFailure."""
    def __init__(self, codebase='', **kwargs):
        self.codebase = codebase
        SetPropertyFromCommand.__init__(self,
                property="got_revision",
                command=["git", "rev-parse", "HEAD"], **kwargs)

    def setProperty(self, propname, value, source):
        """Overridden to set got revision for codebase, if applicable"""
        if self.codebase != '':
            property_dict = self.getProperty(propname, {})
            property_dict[self.codebase] = value
            return SetPropertyFromCommand.setProperty(self, propname, property_dict, source)
        return SetPropertyFromCommand.setProperty(self, propname, value, source)

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
    def __init__(self, cdash_projectname, maxFailedTestCount=0, command=None, **kwargs):
        self.warnCount = 0
        self.errorCount = 0
        self.failedTestsCount = 0
        self.maxFailedTestCount = maxFailedTestCount
        self.cdash_projectname = cdash_projectname

        # TODO: we maybe can convert all these arguments to be passed in through
        # the ctest_extra_options file.
        ShellCommand.__init__(self,
                command=makeCTestDashboardCommand,
                **kwargs)

    def _cdash_query(self):
        ctest_build_name = self.getProperty('ctest_build_name')

        query = cdash.Query(project=self.cdash_projectname)
        query.add_filter(('buildname/string', cdash.StringOp.STARTS_WITH, ctest_build_name))
        query.add_filter(('buildstarttime/date', cdash.DateOp.IS_AFTER, self.getProperty('cdash_time')))

        return query

    def startCommand(self, command, warnings):
        # add a link to summary on cdash.
        cdash_root = self.getProperty('cdash_url')
        self.addURL("cdash", self._cdash_query().get_url('%s/index.php' % cdash_root))

        ShellCommand.startCommand(self, command, warnings)

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

        failed_tests = []

        read_warning_summary = False
        read_error_summary = False
        read_test_summary = False
        read_failed_tests_header = False
        errorsRe = re.compile(r"(\d+) Compiler errors")
        warningsRe = re.compile(r"(\d+) Compiler warnings")
        testRe = re.compile(r"(\d+)% tests passed, (\d+) tests failed out of (\d)+")
        failedTestsStartRe = re.compile(r"The following tests FAILED:")
        failedTestRe = re.compile(r"(\d)+ - ([^ ]+)")
        for line in log.readlines():
            line = line.strip()
            if not read_warning_summary:
                g = warningsRe.match(line)
                if g:
                    self.warnCount = int(g.group(1))
                    read_warning_summary = True
                    continue
            if not read_error_summary:
                g = errorsRe.match(line)
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
            if not read_failed_tests_header:
                g = failedTestsStartRe.match(line)
                if g:
                    read_failed_tests_header = True
                    continue
            elif len(failed_tests) < self.failedTestsCount:
                g = failedTestRe.match(line)
                if g:
                    failed_tests.append(g.group(2))
                    continue

        # Set property a with the failed tests for steps downstream.
        self.setProperty("ctest_failed_tests", failed_tests, "CTestDashboard")

        cdash_root = self.getProperty('cdash_url')
        cdash_index_url = '%s/index.php' % cdash_root
        cdash_test_url = '%s/queryTests.php' % cdash_root

        query = self._cdash_query()

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
        if self.errorCount or self.failedTestsCount > self.maxFailedTestCount:
            return FAILURE
        if self.warnCount or self.failedTestsCount:
            return WARNINGS
        return SUCCESS

@properties.renderer
def makeExtraOptionsString(props):
    props_dict = {
        'prop:model' : 'Experimental',
        'prop:ctest_empty_binary_directory': False,
        'prop:ctest_local_extra_options_file': '',
        'prop:sourcedir' : "source",
        'prop:ctest_test_timeout' : 180, # 3 mins default timeout.
        'prop:ctest_track' : "buildbot",
        'prop:ctest_track_suffix' : '',
    }
    for (key, (value, source)) in props.asDict().iteritems():
        if isinstance(value, str):
            value = value.replace("\\", '/')
        props_dict["prop:%s" % key] = value
    configure_arguments = ['-D%s=%s' % i for i in props.getProperty('configure_options', {}).items()]
    if props.hasProperty('configure_initial_cache'):
        configure_arguments += ['-C', props.getProperty('configure_initial_cache')]
    configure_arguments += props.getProperty('configure_arguments', [])
    props_dict['ctest_configure_options'] = ';'.join(configure_arguments)
    props_dict['ctest_test_excludes'] = '|'.join(props.getProperty('test_excludes'))
    props_dict['ctest_test_includes'] = '|'.join(props.getProperty('test_includes', []))
    if props.getProperty('ignore_exclusions', False):
        props_dict['ctest_test_includes'] = props_dict['ctest_test_excludes']
        props_dict['ctest_test_excludes'] = ''
    props_dict['ctest_parallel_level'] = 1
    if props.getProperty('supports_parallel_testing', False):
        props_dict['ctest_parallel_level'] = props.getProperty('maximum_parallel_level',1)
    props_dict['ctest_test_include_labels'] = '|'.join(props.getProperty('test_include_labels'))
    props_dict['ctest_upload_file_patterns'] = ';'.join(props.getProperty('upload_file_patterns'))
    return """
            # Essential options.
            set (CTEST_COMMAND "%(prop:cmakeroot)s/bin/ctest")
            set (CTEST_SOURCE_DIRECTORY "%(prop:builddir)s/%(prop:sourcedir)s")
            set (CTEST_BINARY_DIRECTORY "%(prop:builddir)s/build")
            set (CTEST_CMAKE_GENERATOR "%(prop:generator)s")

            # we're creating an unique buildname per build.
            # that makes it possible to link back to Cdash summary page easily.
            set (CTEST_BUILD_NAME "%(prop:ctest_build_name)s")
            set (CTEST_SITE "%(prop:slavename)s")

            # the track to submit the dashboard to.
            set (ctest_track "%(prop:ctest_track)s%(prop:ctest_track_suffix)s")

            set (CTEST_BUILD_FLAGS "%(prop:buildflags)s")

            set (CTEST_TEST_TIMEOUT %(prop:ctest_test_timeout)s)

            # Extra configuration options for this build.
            set (ctest_model "%(prop:model)s")

            # Options to pass to the configure stage.
            set (ctest_configure_options "%(ctest_configure_options)s")

            # Test includes
            set (ctest_test_includes "%(ctest_test_includes)s")

            # Test excludes
            set (ctest_test_excludes "%(ctest_test_excludes)s")

            # Tests in parallel -- how many processes to use
            set (ctest_parallel_level "%(ctest_parallel_level)d")

            # Test include labels
            set (ctest_test_include_labels "%(ctest_test_include_labels)s")

            set (ctest_upload_file_patterns "%(ctest_upload_file_patterns)s")

            set (ctest_use_empty_binary_directory "%(prop:ctest_empty_binary_directory)s")

            set (ctest_local_extra_options_file "%(prop:ctest_local_extra_options_file)s")
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

class GetShortRevision(object):
    """Makes is possible to render a short version of a source property. Used by
    SetCTestBuildNameProperty"""
    implements(properties.IRenderable)
    def __init__(self, step):
        self.step = step

    def getRenderingFor(self, props):
        codebases = self.step.codebases
        if not codebases or (len(codebases) == 1 and codebases[0] == ''):
            return props.getProperty("got_revision")[0:8]
        retVal = []
        for codebase in codebases:
            retVal.append(props.getProperty("got_revision")[codebase][0:8])
        return "-".join(retVal)


class SetCTestBuildNameProperty(SetProperty):
    """BuildStep to add a ctest_build_name property to the build.
    The rules used to name the build are as follows:

    * The prefix is defined by:
        - If there's 1 codebase (or no codebase) provided, then the prefix is
          short-rev for the change.
        - If more than one codebase is provided, then the prefix is a '-'
          seperated short-revs for each codebase's change.
    * The suffix is the source_branch property, if present.
    GitlabMergeRequestPoller puts that property when a merge-request produces
    the change object."""
    def __init__(self, codebases=[], property=None, value=None, **kwargs):
        if not property is None or not value is None:
            raise RuntimeError("Unexpected arguments!!!")
        self.codebases = codebases
        SetProperty.__init__(self,
                property="ctest_build_name",
                value=Interpolate("%(kw:shortrevision)s-build%(prop:buildnumber)s-%(prop:buildername)s%(prop:source_branch:?|-%(prop:source_branch)s|)s",
                    shortrevision=GetShortRevision(self)))
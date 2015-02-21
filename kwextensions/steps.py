from buildbot.steps.source.git import Git
from buildbot.process import properties
from buildbot.steps.shell import WarningCountingShellCommand
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.transfer import FileDownload, StringDownload

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


class CTestDashboard(WarningCountingShellCommand):
    name="build-n-test"
    description="building-n-testing"
    descriptionDone="built and tested"
    def __init__(self, model="Experimental", command=None, properties={}, **kwargs):
        WarningCountingShellCommand.__init__(self,
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
                    Interpolate('ctest_test_args_file:STRING=%(prop:workdir)s/ctest_test_args.cmake'),
                    '-S',
                    Interpolate('%(prop:workdir)s/common.ctest')],
                **kwargs)

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
                lines.append("-D%s=%s" % (m.group(1), str(value)))
        return ";".join(lines)
    return makeCommand


class CTestConfigureOptionsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=_get_config_contents(prefix='cc', patternstr='-D%s=%s', joinstr=';'),
                slavedest=Interpolate("%(prop:workdir)s/ctest_configure_options.cmake"),
                **kwargs)

class CTestTestArgsDownload(StringDownload):
    def __init__(self, s=None, slavedest=None, **kwargs):
        StringDownload.__init__(self,
                s=_get_config_contents(prefix='ct', patternstr='%s %s', joinstr=" "),
                slavedest=Interpolate("%(prop:workdir)s/ctest_test_args.cmake"),
                **kwargs)

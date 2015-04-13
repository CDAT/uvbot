"""GeoJS test factory."""

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.transfer import StringDownload

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

import projects
from . import poll

_script = '''#!/bin/bash

port=${1:-50100}
log=out-$$.log

if curl http://$(hostname):$port &> /dev/null ; then
  echo "ERROR: Webserver already running at this port!"
  exit 1
fi

echo "Starting a test server at http://$(hostname):$port/"
./node_modules/.bin/grunt serve-test --port $port &> $log &
echo $! > .pid-$port

for ((i = 0; i < 5; i++)) ; do
  sleep 5
  if curl http://$(hostname):$port &> /dev/null ; then
    echo "Success!"
    exit 0;
  fi
done
cat out-$$.log
rm -f out$$.log
echo "Couldn't start a server on port $port"
rm -f .pid-$port
exit 1
'''


class StartWebServer(ShellCommand):

    """Starts up a web server in the background."""

    script = _script

    def __init__(self, **kw):
        """Create the shell command."""
        # port =Interpolate(
        #     '%(slave:selenium)s'
        # )
        port = 8101
        kw['command'] = 'chmod +x server.sh;  ./server.sh ' + str(port)
        kw['description'] = 'Starting a web server on port {}'.format(port)
        kw['descriptionDone'] = 'Web server started on port {}'.format(port)

        super(StartWebServer, self).__init__(**kw)


class KillWebServer(ShellCommand):

    """Kills a web server."""

    def __init__(self, **kw):
        """Create the shell command."""
        # port = Interpolate(
        #     '%(slave:selenium)s'
        # )
        port = 8101
        kw['command'] = 'kill `cat .pid-{}`'.format(port)
        kw['description'] = 'Killing the web server on port {}'.format(port)
        kw['descriptionDone'] = 'Web server killed'.format(port)
        kw['alwaysRun'] = True

        super(KillWebServer, self).__init__(**kw)


def get_source_steps(sourcedir="source"):
    """Return a list of steps needed to checkout the source properly.

    @param sourcedir is the directory where to checkout the source.
    """
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(
        repourl=poll.REPO_SITE,
        mode='incremental',
        method='clean',
        submodules=True,
        workdir=sourcedir,
        reference=Property("referencedir"),
        codebase=codebase,
        env={'GIT_SSL_NO_VERIFY': 'true'}
    )
    steps = []
    steps.append(update)
    steps.append(
        SetProperty(
            name="SetGeoJSSourceDir",
            property="sourcedir",
            value=sourcedir
        )
    )
    return steps


def get_factory(buildset):
    """Argument is the selected buildset.

    That could be used to build the factory as needed.
    """
    codebase = projects.get_codebase_name(poll.REPO)
    factory = BuildFactory()
    for step in get_source_steps():
        factory.addStep(step)

    # remove dist directory
    factory.addStep(
        RemoveDirectory(
            dir="source/dist",
            flunkOnFailure=False
        )
    )

    # install deps
    factory.addStep(
        ShellCommand(
            command=["npm", "install"],
            workdir="source"
        )
    )

    # build web
    factory.addStep(
        ShellCommand(
            command=["./node_modules/.bin/grunt"],
            workdir="source"
        )
    )

    # build docs
    factory.addStep(
        ShellCommand(
            command=["./node_modules/.bin/grunt", "docs"],
            workdir="source"
        )
    )

    # transfer server script
    factory.addStep(
        StringDownload(
            StartWebServer.script,
            slavedest='server.sh',
            workdir='source'
        )
    )

    # start up server
    factory.addStep(
        StartWebServer(
            workdir='source'
        )
    )

    factory.addStep(SetCTestBuildNameProperty(codebases=[codebase]))
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
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME))

    # kill the web server
    factory.addStep(
        KillWebServer(
            workdir='source'
        )
    )
    return factory

__all__ = [
    "get_factory",
    "get_source_steps"
]

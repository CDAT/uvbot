import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # QtTesting has some issue with playback/capture for this
        # one. We'll fix it at some point
        'TestPythonView',
    ],

    'configure_options:builderconfig': {
        # SVN is too old.
        'DIY_SKIP_SVN:BOOL': 'ON',

        'download_location:PATH': '/home/kitware/Dashboards/downloads/paraview',

        'SUBPROJECT_GENERATOR:STRING': 'Unix Makefiles',
        'SUBPROJECT_BUILD_FLAGS:STRING': '-j3',
    },

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave, paraviewsuperbuild, buildsets, defprops)

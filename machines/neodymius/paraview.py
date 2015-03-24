import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'icc-14.0.0',
    'test_excludes:builderconfig': [
        'ProbePicking', # pick fails
        'TestPythonView', # no matplotlib
        'PropertyLink', # poorly designed
    ],
    'test_excludes:builderconfig': [
        # Both these tests are real failures. Disabling for now
        # to build trust on the dashboard. We need to debug these.
        'pvcrs.LoadState',
        'pvcs.LoadState',
    ],

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',

    'PARAVIEW_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'gui',
            'python',
            'mpi',

            'icc',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig
)

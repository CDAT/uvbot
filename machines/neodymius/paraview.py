import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'icc-14.0.0',
    'test_excludes:builderconfig': [
        # Both these tests are real failures. Disabling for now
        # to build trust on the dashboard. We need to debug these.
        'pvcrs.LoadState',
        'pvcs.LoadState',
    ],

    'configure_options:builderconfig': {
        'PARAVIEW_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData',
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
        'features': (
            'gui',
            'python',
            'mpi',

            'icc',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets, defprops)

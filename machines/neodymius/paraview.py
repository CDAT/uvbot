import projects
from projects import paraview

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        'ProbePicking', # pick fails
        'TestPythonView', # no matplotlib
    ],
    'env': {
        'DISPLAY': ':0',
        'CC': 'icc',
        'CXX': 'icpc',
    },
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',

    'PARAVIEW_DATA_STORE:PATH': '%(prop:sharedresourcesroot)s/ExternalData',
}

buildsets = [
    {
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'gui',
            'python',
            'mpi',
        ),
    },
]

BUILDERS = projects.make_builders(paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['neodymius']
)

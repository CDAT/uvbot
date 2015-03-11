import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'referencedir': '/home/kitware/dashboards/buildbot-share/vtk',
}
env = {
    'DISPLAY': ':1',
    'PATH': '/usr/lib64/mpich/bin:${PATH}',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',
    'VTK_ENABLE_CATALYST:BOOL': 'ON',

    'VTK_DATA_STORE:PATH': '/home/kitware/dashboards/data/vtk',

    # Breaks sanitizers with its segfault testing.
    'VTK_USE_SYSTEM_HDF5:BOOL': 'ON',
}

base_features = (
    'python',
    'qt',
    'qt5',
    'mpi',
)
buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)

sanitizers = '-fsanitize=address,undefined'

sanbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'relwithdebinfo',
        'features': base_features + (
            'asan',
            'ubsan',
        ),
    },
]
sanenv = projects.merge_config(env, {
    'CFLAGS': sanitizers,
    'CXXFLAGS': sanitizers,
    'LDFLAGS': sanitizers,
})

BUILDERS += projects.make_builders(slave.SLAVE, vtk, sanbuildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=sanenv
)

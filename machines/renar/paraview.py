import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'gcc-4.8.2',
    'configure_options:builderconfig': {
        'PARAVIEW_DATA_STORE:PATH': '/home/kitware/ParaViewExternalData',
     },

     'slaveenv': {
        'DISPLAY': ':0',
        # Rob says you have to specify these since /usr/bin/cc changes
        'CC': 'gcc-4.8',
        'CXX': 'g++-4.8',
     },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'debug',
        'category': 'experimental',
        'features': (
            'gui',
            'python',
            'mpi',
            'opengl2',
        ),
    },
]

BUILDERS = projects.make_builders(slave, paraview, buildsets, defprops)

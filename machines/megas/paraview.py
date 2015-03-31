import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # broken selection on VNC
        'TestYoungsMaterialInterface',
        'NonlinearSubdivisionDisplay',

        'TestWindowToImageTransparency', # broken transparency on VNC(?)
        'rendererSource', # broken stencil buffer on VNC(?)
        'FindWidget', # X errors
        'EyeDomeLighting', # unsupported texture format
        'SelectionLabels', # http://www.paraview.org/Bug/view.php?id=15294
    ],

    'configure_options:builderconfig': {
        'PARAVIEW_DATA_STORE:PATH': '/home/kitware/dashboards/data/paraview',

        'PARAVIEW_USE_VISITBRIDGE': 'ON',
    },

    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',

    'slaveenv': {
        'DISPLAY': ':1',
        'PATH': '/usr/lib64/mpich/bin:${PATH}',
    },
}

base_features = (
    'gui',
    'python',
    'kits',
    'mpi',
)
buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave, paraview, buildsets, defprops)

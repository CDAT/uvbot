import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # broken selection on VNC
        'TestYoungsMaterialInterface',

        'TestWindowToImageTransparency', # broken transparency on VNC(?)
        'rendererSource', # broken stencil buffer on VNC(?)

        # FIXME: probably broken
        'vtkInteractionWidgetsCxx-TestDijkstraImageGeodesicPath',
        'vtkInteractionWidgetsCxx-TestImageActorContourWidget',
        'vtkRenderingCoreCxx-TestTilingCxx',
        'vtkRenderingOpenGLCxx-TestValuePainter',
    ],

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/home/kitware/dashboards/data/vtk',
    },

    'referencedir': '/home/kitware/dashboards/buildbot-share/vtk',

    'slaveenv': {
        'DISPLAY': ':1',
        'PATH': '/usr/lib64/mpich/bin:${PATH}',
    },
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
        'features': base_features + (
            '_strict',
        ),
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)

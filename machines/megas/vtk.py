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
    'referencedir': '/home/kitware/dashboards/buildbot-share/vtk',
}
env = {
    'DISPLAY': ':1',
    'PATH': '/usr/lib64/mpich/bin:${PATH}',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
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

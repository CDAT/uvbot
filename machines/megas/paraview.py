import projects
from projects import paraview

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_include_labels:builderconfig': [
        'PARAVIEW',
    ],
    'test_excludes:builderconfig': [
        # broken selection on VNC
        'TestYoungsMaterialInterface',
        'NonlinearSubdivisionDisplay',

        'TestWindowToImageTransparency', # broken transparency on VNC(?)
        'rendererSource', # broken stencil buffer on VNC(?)
        'FindWidget', # X errors
        'EyeDomeLighting', # unsupported texture format
    ],
}
env = {
    'DISPLAY': ':1',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',
    'VTK_ENABLE_CATALYST:BOOL': 'ON',

    'PARAVIEW_DATA_STORE:PATH': '/home/kitware/dashboards/data',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'gui',
            'python',
            'kits',
            'mpi',
        ),
    },
]

BUILDERS = projects.make_builders(paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['megas'],
    env=env
)

from buildbot.process.properties import Interpolate

import projects
from projects import paraview

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_include_labels:builderconfig': [
        'PARAVIEW',
        'CATALYST',
        'PARAVIEWWEB',
    ],
    'test_excludes:builderconfig': [
        'ProbePicking', # flaky
        'TestPythonView', # bad on OS X
        'HistogramSelection', # viewport too small (image corruption)
    ],
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',
    'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
    'PARAVIEW_ENABLE_CATALYST:BOOL': 'ON',
    'PARAVIEW_DATA_STORE:PATH': Interpolate('%(prop:sharedresourcesroot)s/data'),

    'VTK_USE_SYSTEM_EXPAT:BOOL': 'ON',
    'VTK_USE_SYSTEM_JPEG:BOOL': 'ON',
    'VTK_USE_SYSTEM_LIBXML2:BOOL': 'ON',
    'VTK_USE_SYSTEM_PNG:BOOL': 'ON',
    'VTK_USE_SYSTEM_TIFF:BOOL': 'ON',
    'VTK_USE_SYSTEM_ZLIB:BOOL': 'ON',
}

base_features = (
    'kits',
    'python',
)
buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features + (),
    },
    {
        'os': 'osx',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features + (),
    },
]

BUILDERS = projects.make_builders(paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['trey']
)

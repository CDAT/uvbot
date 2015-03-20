import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_include_labels:builderconfig': [
        'PARAVIEW',
    ],
    'test_excludes:builderconfig': [
        # TODO: Why are these excluded?
        'EyeDomeLighting',
        'NewColorEditor1',
        'pvcs-tile-display',
        'CTHAMRMaterialInterfaceFilter',
        'CreateDelete',
        'pvcs.StructuredGridVolumeRendering',
        'UncertaintyRendering',
        'DisconnectAndSaveAnimation',
        'NonlinearSubdivisionDisplay',
        'StereoSplitViewportHorizontal',
    ],
}
env = {
    'PATH': 'C:/Support/Qt/4.8.0-vs2010-x64/bin;C:/Python27x64;${PATH}',
}

defconfig = {
    'CMAKE_CXX_MP_FLAG:BOOL': 'ON',

    'BUILD_TESTING:BOOL': 'OFF',
    'BUILD_EXAMPLES:BOOL': 'OFF',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',

    'VTK_DATA_STORE:PATH': 'C:/Dashboards/CDashHome/ExternalData',

    'Boost_INCLUDE_DIR:PATH': 'C:/Support/boost_1_48_0',

    'PARAVIEW_USE_VISITBRIDGE:BOOL': 'ON',
    'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
}

base_features = (
    'gui',
    'mpi',
    'vs',
)
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features,
    },
    {
        'os': 'windows',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)

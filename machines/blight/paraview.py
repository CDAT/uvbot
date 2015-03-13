import projects
from projects import paraview
from . import slave

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
        # TODO: Why are these disabled?
        'AnimatePipelineTime',
        'CreateDelete',
        'EyeDomeLighting',
        'IceTOddImageSizes',
        'SurfaceLIC',
        'TestIceTCompositePassWithBlurAndOrderedCompositing',
        'TestIceTCompositePassWithSobel',
        'TestIceTShadowMapPass-image',
        'UncertaintyRendering',
        'Visualizer-renderer_click',
        'pvcs.StructuredGridVolumeRendering',
        'pvweb-chrome.TestApp-all',
    ],
}
env = {
    'DISPLAY': ':0',
    # since we're using mesa, no need to do offscreen screenshots.
    'PV_NO_OFFSCREEN_SCREENSHOTS': '1',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
    'PARAVIEW_DATA_STORE:PATH': '/home/kitware/Dashboards/MyTests/ExternalData',

    'PARAVIEW_BUILD_PLUGIN_MantaView:BOOL': 'ON',
    'MANTA_BUILD:PATH': '/opt/source/manta-build',

    'smooth_flash:FILEPATH': '/home/kitware/Dashboards/MyTests/ParaViewSuperLargeData/smooth.flash',

    'PARAVIEW_ENABLE_COSMOTOOLS:BOOL': 'ON',
    'GENERIC_IO_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Support/Cosmology/genericio',
    'GENERIC_IO_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/genericio-build/libGenericIO.a',
    'COSMOTOOLS_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/include',
    'COSMOTOOLS_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/libs/libcosmotools.a',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'debug',
        'features': (
            'gui',
            'python',
            'mpi',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': (
            'gui',
            'python',
            'mpi',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': (
            'python',
            'mpi',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'mpi',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': (),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)

qt5props = projects.merge_config(defprops, {
    'test_excludes:builderconfig': [
        # This fails with an assertion. This really needs
        # to be debugged before we make Qt5 the default.
        'pv.LoadPlugins',
    ]
})
qt5env = projects.merge_config(env, {
    'PATH': '/opt/apps/qt-5.3.1/bin:${PATH}',
    'LD_LIBRARY_PATH': '/opt/apps/qt-5.3.1/lib:${LD_LIBRARY_PATH}',
    'CMAKE_PREFIX_PATH': '/opt/apps/qt-5.3.1/lib/cmake:${CMAKE_PREFIX_PATH}',
})

qt5buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'gui',
            'qt5',
        )
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, paraview, qt5buildsets,
    defprops=qt5props,
    defconfig=defconfig,
    env=qt5env
)

r"""
    Machine: blight.kitware.com
    Owner: utkarsh.ayachit@kitware.com
"""

from buildbot.buildslave import BuildSlave

# Slave configuration for the machine.
slave = BuildSlave("blight", "XXXXXXXX",
        max_builds=1,
        properties = {
            'cmakeroot': "/opt/apps/cmake-3.0.1",
            'sharedresourcesroot': "/home/kitware/Dashboards/MyTests",

            'os' : 'linux',
            'distribution' : 'Ubuntu-12.04 64 bit',
            'compiler' : 'gcc-4.6.3',
            "generator" : "Unix Makefiles",

            # Add site-specific cmake options here.
            'configure_options:buildslave' : {
                'CMAKE_CXX_FLAGS:STRING': "-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated",
                'CMAKE_C_FLAGS:STRING': "-Wall -Wextra -Wshadow",
                'BUILD_EXAMPLES:BOOL': 'ON',
                'VTK_DEBUG_LEAKS:BOOL' : 'ON',
                'PARAVIEW_BUILD_PLUGIN_MantaView:BOOL' : 'ON',
                'MANTA_BUILD:PATH' :'/opt/source/manta-build',
                'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL' : 'ON',
                'smooth_flash:FILEPATH' : '/home/kitware/Dashboards/MyTests/ParaViewSuperLargeData/smooth.flash',
                'PARAVIEW_ENABLE_COSMOTOOLS:BOOL' : 'ON',
                'GENERIC_IO_INCLUDE_DIR:PATH' : '/home/kitware/Dashboards/Support/Cosmology/genericio',
                'GENERIC_IO_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/genericio-build/libGenericIO.a',
                'COSMOTOOLS_INCLUDE_DIR:PATH' : '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/include',
                'COSMOTOOLS_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/libs/libcosmotools.a',

                # setup some default values for these overridables.
                'CMAKE_BUILD_TYPE:STRING' : 'Debug',
                "PARAVIEW_BUILD_QT_GUI:BOOL" : "ON",
            },

            # Add test options.
            'test_excludes:buildslave' : ['CreateDelete',
                                     'TestIceTCompositePassWithBlurAndOrderedCompositing',
                                     'TestIceTCompositePassWithSobel',
                                     'TestIceTShadowMapPass-image',
                                     'IceTOddImageSizes',
                                     'AnimatePipelineTime',
                                     'EyeDomeLighting',
                                     'pvcs.StructuredGridVolumeRendering',
                                     'UncertaintyRendering',
                                     'Visualizer-renderer_click',
                                     'pvweb-chrome.TestApp-all',
                                     'SurfaceLIC']
            }
        )

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

            # Add site-specific options here.
            'cc:CMAKE_CXX_FLAGS:STRING': "-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated",
            'cc:CMAKE_C_FLAGS:STRING': "-Wall -Wextra -Wshadow",
            'cc:PARAVIEW_DISABLE_VTK_TESTING:BOOL':'ON',
            'cc:BUILD_EXAMPLES:BOOL': 'ON',
            'cc:VTK_DEBUG_LEAKS:BOOL' : 'ON',
            'cc:PARAVIEW_BUILD_PLUGIN_MantaView:BOOL' : 'ON',
            'cc:MANTA_BUILD:PATH' :'/opt/source/manta-build',
            'cc:PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL' : 'ON',
            'cc:smooth_flash:FILEPATH' : '/home/kitware/Dashboards/MyTests/ParaViewSuperLargeData/smooth.flash',
            'cc:PARAVIEW_ENABLE_COSMOTOOLS:BOOL' : 'ON',
            'cc:GENERIC_IO_INCLUDE_DIR:PATH' : '/home/kitware/Dashboards/Support/Cosmology/genericio',
            'cc:GENERIC_IO_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/genericio-build/libGenericIO.a',
            'cc:COSMOTOOLS_INCLUDE_DIR:PATH' : '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/include',
            'cc:COSMOTOOLS_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/libs/libcosmotools.a',

            # Add test options.
            'ct:EXCLUDE' : 'CreateDelete|TestIceTCompositePassWithBlurAndOrderedCompositing|TestIceTCompositePassWithSobel|TestIceTShadowMapPass-image|IceTOddImageSizes|AnimatePipelineTime|EyeDomeLighting|pvcs.StructuredGridVolumeRendering|UncertaintyRendering|Visualizer-renderer_click|pvweb-chrome.TestApp-all|SurfaceLIC'
            }
        )

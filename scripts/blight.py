r"""
    Machine: blight.kitware.com
    Owner: utkarsh.ayachit@kitware.com
"""

from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from kwextensions import factory
from buildbot.process.properties import Property, Interpolate

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

build_configurations = {
        'shared-python-mpi-debug' : {
            "BUILD_SHARED_LIBS:BOOL" : "ON",
            "PARAVIEW_ENABLE_PYTHON:BOOL" : "OFF",
            "PARAVIEW_USE_MPI:BOOL" : "ON",
            'CMAKE_BUILD_TYPE:STRING' : 'Debug'
            },
        'static-python-mpi-release' : {
            "BUILD_SHARED_LIBS:BOOL" : "OFF",
            "PARAVIEW_ENABLE_PYTHON:BOOL" : "OFF",
            "PARAVIEW_USE_MPI:BOOL" : "ON",
            'CMAKE_BUILD_TYPE:STRING' : 'Release'
            },
        'static-python-mpi-nogui-release' : {
            "BUILD_SHARED_LIBS:BOOL" : "OFF",
            "PARAVIEW_ENABLE_PYTHON:BOOL" : "OFF",
            "PARAVIEW_USE_MPI:BOOL" : "ON",
            "PARAVIEW_BUILD_QT_GUI:BOOL" : "OFF",
            'CMAKE_BUILD_TYPE:STRING' : 'Release'
            },
        'shared-python-mpi-nogui-release' : {
            "BUILD_SHARED_LIBS:BOOL" : "ON",
            "PARAVIEW_ENABLE_PYTHON:BOOL" : "OFF",
            "PARAVIEW_USE_MPI:BOOL" : "ON",
            "PARAVIEW_BUILD_QT_GUI:BOOL" : "OFF",
            'CMAKE_BUILD_TYPE:STRING' : 'Release'
            }
        }

builders = {}
builders["ParaView"] = []
for key, configure_options in build_configurations.iteritems():
    properties = {}
    # add the cmake configure options
    properties['configure_options:builderconfig'] = configure_options

    # add a list of test include labels
    properties["test_include_labels:builderconfig"] = ['PARAVIEW', 'CATALYST', 'PARAVIEWWEB']
    builders["ParaView"].append(
            BuilderConfig(name="linux-%s" % key,
                slavenames=["blight"],
                factory=factory.get_ctest_buildfactory(),
                properties = properties,
                env= {"DISPLAY" : ":0",
                    "ExternalData_OBJECT_STORES": Interpolate("%(prop:sharedresourcesroot)s/ExternalData")
                    }
                ))

builders["ParaViewSuperbuild"]=[]
builders["ParaViewSuperbuild"].append(
        BuilderConfig(name="ubuntu12.04-shared-superbuild",
            slavenames=["blight"],
            factory=factory.get_ctest_buildfactory(),
            properties = {
                'configure_options:builderconfig' : {
                    "BUILD_SHARED_LIBS:BOOL" : "ON",
                    'CMAKE_BUILD_TYPE:STRING' : 'Release',
                    "USE_NONFREE_COMPONENTS:BOOL":"ON",
                    "ENABLE_acusolve:BOOL":"ON",
                    "ENABLE_boost:BOOL":"ON",
                    "ENABLE_cgns:BOOL":"ON",
                    "ENABLE_cosmotools:BOOL":"ON",
                    "ENABLE_ffmpeg:BOOL":"ON",
                    "ENABLE_manta:BOOL":"ON",
                    "ENABLE_matplotlib:BOOL":"ON",
                    "ENABLE_mpi:BOOL":"ON",
                    "ENABLE_nektarreader:BOOL":"ON",
                    "ENABLE_numpy:BOOL":"ON",
                    "ENABLE_paraview:BOOL":"ON",
                    "ENABLE_python:BOOL":"ON",
                    "ENABLE_qt:BOOL":"ON",
                    "ENABLE_silo:BOOL":"ON",
                    "ENABLE_visitbridge:BOOL":"ON",
                    "ENABLE_vistrails:BOOL":"ON",
                    "PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL":"ON",
                    "download_location:PATH":"/home/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads"
                    }
                }
            )
        )

def get_buildslave():
    """Returns the BuildSlave instance for this machine"""
    return slave

def get_builders(project="ParaView"):
    """Returns a list of build configurations for this slave for a specific project."""
    return builders[project]

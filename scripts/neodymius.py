from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from kwextensions import factory
from buildbot.process.properties import Property, Interpolate

slave = BuildSlave('neodymius', 'XXXXXXXX',
        max_builds=1,
        properties = {
            'cmakeroot': "/usr",
            'sharedresourcesroot': "/home/kitware/Dashboards",

            'os' : 'linux',
            'distribution' : 'Fedora?',
            'compiler' : 'icc',
            "generator" : "Makefiles",

            # Add site-specific cmake options here.
            'configure_options:buildslave' : {
                "CMAKE_CXX_FLAGS:STRING"  : "-Wall -Wextra -Wno-shadow -Wno-unused-function -Woverloaded-virtual -Wno-deprecated",
                "CMAKE_C_FLAGS:STRING" : "-Wall -Wextra -Wno-shadow -Wno-unused-function",
                "MPIEXEC:FILEPATH" : "mpiexec.hydra",
                "PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL" : "ON"

                "BUILD_EXAMPLES:BOOL" : "ON",
                "BUILD_SHARED_LIBS:BOOL" : "ON",
                'CMAKE_BUILD_TYPE:STRING' : 'Release',
                "PARAVIEW_ENABLE_PYTHON:BOOL" : "ON",
                "PARAVIEW_USE_MPI:BOOL" : "ON",
                "VTK_DEBUG_LEAKS:BOOL"  : "ON",
                },
            'test_excludes:buildslave' : [
                #  ProbePicking -- pick fails
                "ProbePicking",
                # TestPythonView -- no matplotlib
                "TestPythonView"
                ]
        )

builders = {}
builders["ParaView"] = [
    BuilderConfig(name="linux-icc-shared-python-mpi-release",
        slavenames=["neodymius"],
        factory=factory.get_ctest_buildfactory(),
        properties = {},
        env = {'CC' : 'icc', 'CXX' : 'icpc'}
        )
    ]

def get_buildslave():
    """Returns the BuildSlave instance for this machine"""
    return slave

def get_builders(project="ParaView"):
    """Returns a list of build configurations for this slave for a specific project."""
    try:
        return builders[project]
    except KeyError:
        return []

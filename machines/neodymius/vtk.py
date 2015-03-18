import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'icc-14.0.0',
}
env = {
    'DISPLAY': ':0',
    'CC': 'icc',
    'CXX': 'icpc',
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',

    'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData/vtk',
}

allconfig = projects.merge_config(defconfig, {
    'VTK_BUILD_ALL_MODULES:BOOL': 'ON',
    'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
})

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'tcl',
            'java',

            'icc',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=allconfig,
    env=env
)

glnewprops = projects.merge_config(defprops, {
    'compiler': 'gcc-4.8.3',
    'ctest_track' : 'VolumeOpenGLNew',
})
glnewenv = projects.merge_config(env, {
    'CC': 'gcc',
    'CXX': 'g++',
})

glnewconfig = projects.merge_config(defconfig, {
    'Moddule_vtkRenderingVolumeOpenGLNew:BOOL': 'ON',
})

glnewbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'tcl',
            'java',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, vtk, glnewbuildsets,
    defprops=glnewprops,
    defconfig=glnewconfig,
    env=glnewenv
)

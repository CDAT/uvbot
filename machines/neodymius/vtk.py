import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'icc-14.0.0',

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData/vtk',
    },

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

allprops = projects.merge_config(defprops, {
    'configure_options:builderconfig': {
        'VTK_BUILD_ALL_MODULES:BOOL': 'ON',
        'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
    },
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

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets, allprops)

glnewprops = projects.merge_config(defprops, {
    'compiler': 'gcc-4.8.3',
    'ctest_track' : 'VolumeOpenGLNew',

    'configure_options:builderconfig': {
        'Module_vtkRenderingVolumeOpenGLNew:BOOL': 'ON',
    },
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

BUILDERS += projects.make_builders(slave.SLAVE, vtk, glnewbuildsets, glnewprops)

import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'compiler': 'clang-apple-3.1',
    'test_excludes:builderconfig': [
        # Old GPU drivers.
        'vtkRenderingVolumePython-volTM2DRotateClip',
    ],

    'slaveenv': {
        'DYLD_LIBRARY_PATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++:${DYLD_LIBRARY_PATH}',
        'PATH': '/Users/kitware/Dashboards/Support/openmpi/bin:${PATH}',
    },
}

defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'BUILD_TESTING:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',
    'VTK_DATA_STORE:PATH': '/Users/kitware/Dashboards/ExternalData',
    'VTK_USER_LARGE_DATA:BOOL': 'ON',

    'Module_vtkIOXdmf2:BOOL': 'ON',
    'Module_vtkIOGDAL:BOOL': 'ON',
    'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',

    'MPIEXEC:FILEPATH': '/Users/kitware/Dashboards/Support/openmpi/bin/orterun',
    'QT_QMAKE_EXECUTABLE:PATH': '/Users/kitware/Dashboards/Support/Qt-4.8.0/bin/qmake',
    'VTK_GHOSTSCRIPT_EXECUTABLE:FILEPATH': '/Users/kitware/david.lonie/ghostscript-9.06/bin/gs',

    'VTK_SMP_IMPLEMENTATION_TYPE:STRING': 'TBB',
    'TBB_INSTALL_DIR:PATH': '/Users/kitware/Dashboards/Support/tbb',
    'TBB_INCLUDE_DIR:PATH': '/Users/kitware/Dashboards/Support/tbb/include',
    'TBB_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbb.dylib',
    'TBB_MALLOC_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbbmalloc.dylib',
    'TBB_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbb_debug.dylib',
    'TBB_MALLOC_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbbmalloc_debug.dylib',
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'clang',
            'java',
            'mpi',
            'python',
            'qt',
            'tbb',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtk, buildsets,
    defprops=defprops,
    defconfig=defconfig
)

gccprops = projects.merge_config(defprops, {
    'compiler': 'gcc-4.2.1',

    'slaveenv': {
        'DYLD_LIBRARY_PATH': '/Users/kitware/Dashboards/Support/tbb/lib:${DYLD_LIBRARY_PATH}',
        'CC': 'gcc',
        'CXX': 'g++',
    },
})
gccconfig = projects.merge_config(defconfig, {
    'TBB_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbb.dylib',
    'TBB_MALLOC_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbbmalloc.dylib',
    'TBB_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbb_debug.dylib',
    'TBB_MALLOC_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbbmalloc_debug.dylib',
})

gccbuildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'java',
            'mpi',
            'python',
            'tbb',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, vtk, gccbuildsets,
    defprops=defprops,
    defconfig=gccconfig
)

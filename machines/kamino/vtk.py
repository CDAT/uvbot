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

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/Users/kitware/Dashboards/ExternalData',

        'Module_vtkIOXdmf2:BOOL': 'ON',
        'Module_vtkIOGDAL:BOOL': 'ON',
        'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',

        'MPIEXEC:FILEPATH': '/Users/kitware/Dashboards/Support/openmpi/bin/orterun',
        'QT_QMAKE_EXECUTABLE:PATH': '/Users/kitware/Dashboards/Support/Qt-4.8.0/bin/qmake',
        'VTK_GHOSTSCRIPT_EXECUTABLE:FILEPATH': '/Users/kitware/david.lonie/ghostscript-9.06/bin/gs',

        'TBB_INSTALL_DIR:PATH': '/Users/kitware/Dashboards/Support/tbb',
        'TBB_INCLUDE_DIR:PATH': '/Users/kitware/Dashboards/Support/tbb/include',
        'TBB_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbb.dylib',
        'TBB_MALLOC_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbbmalloc.dylib',
        'TBB_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbb_debug.dylib',
        'TBB_MALLOC_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++/libtbbmalloc_debug.dylib',
    },

    'slaveenv': {
        'DYLD_LIBRARY_PATH': '/Users/kitware/Dashboards/Support/tbb/lib/libc++:${DYLD_LIBRARY_PATH}',
        'PATH': '/Users/kitware/Dashboards/Support/openmpi/bin:${PATH}',
    },

    'supports_parallel_testing:sandbox': True,
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'category': 'experimental',
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

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)

gccprops = projects.merge_config(defprops, {
    'compiler': 'gcc-4.2.1',

    'configure_options:builderconfig': {
        'TBB_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbb.dylib',
        'TBB_MALLOC_LIBRARY:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbbmalloc.dylib',
        'TBB_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbb_debug.dylib',
        'TBB_MALLOC_LIBRARY_DEBUG:FILEPATH': '/Users/kitware/Dashboards/Support/tbb/lib/libtbbmalloc_debug.dylib',
    },

    'slaveenv': {
        'DYLD_LIBRARY_PATH': '/Users/kitware/Dashboards/Support/tbb/lib:${DYLD_LIBRARY_PATH}',
        'CC': 'gcc',
        'CXX': 'g++',
    },
})

gccbuildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'category': 'experimental',
        'features': (
            'java',
            'mpi',
            'python',
            'tbb',
        ),
    },
]

BUILDERS += projects.make_builders(slave, vtk, gccbuildsets, gccprops)

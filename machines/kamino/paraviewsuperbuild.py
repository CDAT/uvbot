import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

BUILDERS = []

defprops = {
    'upload_file_patterns:builderconfig': [
        '*.dmg',
        '*.tar.gz',
        '*.tgz',
    ],
    'test_excludes:builderconfig': [
        # QtTesting has some issue with playback/capture for this
        # one on OsX. We'll fix it at some point
        'TestPythonView',
    ],
}

defconfig = {
    'BUILD_TESTING:BOOL': 'ON',

    # CMake is picking make -i as default, which ends up ignoring errors and wasting time!
    'MAKE_COMMAND:STRING': '/usr/bin/make',

    # Manually specify the Fortran compiler.
    'CMAKE_Fortran_COMPILER:FILEPATH': '/usr/local/bin/gfortran',

    'USE_NONFREE_COMPONENTS:BOOL': 'ON',
    'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

    'ENABLE_boost:BOOL': 'ON',
    'ENABLE_cgns:BOOL': 'ON',
    'ENABLE_cosmotools:BOOL': 'ON',
    'ENABLE_ffmpeg:BOOL': 'ON',
    'ENABLE_matplotlib:BOOL': 'ON',
    'ENABLE_mpi:BOOL': 'ON',
    'ENABLE_nektarreader:BOOL': 'ON',
    'ENABLE_numpy:BOOL': 'ON',
    'ENABLE_paraview:BOOL': 'ON',
    'ENABLE_python:BOOL': 'ON',
    'ENABLE_qt:BOOL': 'ON',
    'ENABLE_silo:BOOL': 'ON',
    'ENABLE_visitbridge:BOOL': 'ON',
    'ENABLE_vistrails:BOOL': 'ON',

    'download_location:PATH': '/Users/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads',
}

osx105config = projects.merge_config(defconfig, {
    # Essential variables to ensure that the package can be used on Leopard.
    'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.6.sdk',
    'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',
    'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.5',

    # Force the Python version.
    'PYTHON_EXECUTABLE:FILEPATH': '/usr/bin/python2.6',
    'PYTHON_INCLUDE_DIR:PATH': '/System/Library/Frameworks/Python.framework/Versions/2.6/Headers',
    'PYTHON_LIBRARY:FILEPATH': '/usr/lib/libpython2.6.dylib',
})

osx105buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'osx10.5',
            'superbuild',
        ),
    },
]

# temporarily disabling 10.5 superbuilds. Kamino is too busy. We can only afford
# 1 superbuild at this moment.
#BUILDERS += projects.make_builders(slave.SLAVE, paraviewsuperbuild, osx105buildsets,
#    defprops=defprops,
#    defconfig=osx105config
#)

osx107config = projects.merge_config(defconfig, {
    # Essential variables to ensure that the package can be used on Leopard.
    'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
    'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',
    'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.7',

    # Force the Python version.
    'PYTHON_EXECUTABLE:FILEPATH': '/usr/bin/python2.7',
    'PYTHON_INCLUDE_DIR:PATH': '/System/Library/Frameworks/Python.framework/Versions/2.7/Headers',
    'PYTHON_LIBRARY:FILEPATH': '/usr/lib/libpython2.7.dylib',
})

osx107buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'osx10.7',
            'superbuild',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, paraviewsuperbuild, osx107buildsets,
    defprops=defprops,
    defconfig=osx107config
)

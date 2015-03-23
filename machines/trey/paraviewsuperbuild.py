import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    #  superbuilds only support make files currently.
    'generator': 'Unix Makefiles',

    'upload_file_patterns:builderconfig': [
        '*.dmg',
        '*.tar.gz',
        '*.tgz',
    ],
}

defconfig = {
    'USE_NONFREE_COMPONENTS:BOOL': 'ON',
    'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

    'ENABLE_acusolve:BOOL': 'ON',
    'ENABLE_boost:BOOL': 'ON',
    'ENABLE_cgns:BOOL': 'ON',
    'ENABLE_cosmotools:BOOL': 'ON',
    'ENABLE_ffmpeg:BOOL': 'ON',
    'ENABLE_manta:BOOL': 'ON',
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

    'download_location:PATH': '/Users/kitware/dashboards/paraview-superbuild-downloads',

    # Set OsX SYSROOT, etc.
    'CMAKE_OSX_ARCHITECTURES:STRING' : 'x86_64',
    'CMAKE_OSX_DEPLOYMENT_TARGET:STRING'  : '10.10',
    'CMAKE_OSX_SYSROOT:PATH' : '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk',

    # Pick Python version.
    'PYTHON_EXECUTABLE:FILEPATH' : '/usr/bin/python2.7',
    'PYTHON_INCLUDE_DIR:PATH' : '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk/System/Library/Frameworks/Python.framework/Versions/2.7/Headers',
    'PYTHON_LIBRARY:FILEPATH' : '/usr/lib/libpython2.7.dylib',
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'category': 'experimental',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets,
    defprops=defprops,
    defconfig=defconfig
)

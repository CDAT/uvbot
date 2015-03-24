import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

        'download_location:PATH': '/Users/kitware/dashboards/paraview-superbuild-downloads',

        # Set OS X SYSROOT, etc.
        'CMAKE_OSX_ARCHITECTURES:STRING' : 'x86_64',
        'CMAKE_OSX_DEPLOYMENT_TARGET:STRING'  : '10.10',
        'CMAKE_OSX_SYSROOT:PATH' : '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk',

        # Pick Python version.
        'PYTHON_EXECUTABLE:FILEPATH' : '/usr/bin/python2.7',
        'PYTHON_INCLUDE_DIR:PATH' : '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk/System/Library/Frameworks/Python.framework/Versions/2.7/Headers',
        'PYTHON_LIBRARY:FILEPATH' : '/usr/lib/libpython2.7.dylib',
    },
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

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets, defprops)

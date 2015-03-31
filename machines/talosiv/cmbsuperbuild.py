import projects
from projects import cmbsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.9',

        'ENABLE_hdf5:BOOL': 'ON',

        'USE_SYSTEM_qt:BOOL': 'ON',
        'QT_QMAKE_EXECUTABLE:PATH': '/usr/local/qt-kitware/4.8.6/bin/qmake',

        'PYTHON_EXECUTABLE:FILEPATH': '/usr/bin/python2.7',
        'PYTHON_INCLUDE_DIR:PATH': '/System/Library/Frameworks/Python.framework/Versions/2.7/Headers',
        'PYTHON_LIBRARY:FILEPATH': '/usr/lib/libpython2.7.dylib',
    },
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (),
    },
]

BUILDERS = projects.make_builders(slave, cmbsuperbuild, buildsets, defprops)

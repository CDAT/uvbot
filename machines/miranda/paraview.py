import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

#------------------------------------------------------------------------------
# Common properties and environment.
#------------------------------------------------------------------------------
defprops = {
    'test_excludes:builderconfig': [
        'UncertaintyRendering', # TODO: why?
        'pvcs-collab.CreateDelete', # TODO: why?
        'OpenHelp', # random clucene exceptions
    ],

    'configure_options:builderconfig': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'VTK_LEGACY_REMOVE:BOOL': 'ON',
        'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
        'PARAVIEW_DATA_STORE:PATH': 'C:/Dashboards/data/paraview',
    },

    'slaveenv': {
        'JSDUCK_HOME': 'C:/Tools/jsduck-4.4.1',
    },
}

#------------------------------------------------------------------------------
vs9props = {
    'vcvarsall': 'C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/vcvarsall.bat',
}

#------------------------------------------------------------------------------
ninjaprops = {
    'generator:builderconfig': 'Ninja',
    'buildflags:builderconfig': '-l9',
}

#------------------------------------------------------------------------------
x64props = {
    'generator:builderconfig': 'Visual Studio 9 2008 Win64',
    'buildflags:builderconfig': '',
    'compiler': 'msvc-2008-x64',
    'vcvarsargument': 'amd64',

    'configure_options:builderconfig': {
        'PYTHON_EXECUTABLE:FILEPATH': 'C:/Tools/Python27/x64/python.exe',
        'PYTHON_INCLUDE_DIR:PATH': 'C:/Tools/Python27/x64/include',
        'PYTHON_LIBRARY:FILEPATH': 'C:/Tools/Python27/x64/libs/python27.lib',
    },

    'slaveenv': {
        'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x64/bin;C:/Tools/Python27/x64;${PATH}'
    },
}

x32props = {
    'generator:builderconfig': 'Visual Studio 9 2008',
    'buildflags:builderconfig': '',
    'compiler': 'msvc-2008-x32',
    'vcvarsargument': 'x86',

    'configure_options:builderconfig': {
        # We don't have 32-bit Python on this machine for dashboards.
        #'PYTHON_EXECUTABLE:FILEPATH': 'C:/Tools/Python27/x32/python.exe',
        #'PYTHON_INCLUDE_DIR:PATH': 'C:/Tools/Python27/x32/include',
        #'PYTHON_LIBRARY:FILEPATH': 'C:/Tools/Python27/x32/libs/python27.lib',
    },

    'slaveenv': {
        'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x32/bin;C:/Tools/Python27/x32;${PATH}'
    },
}

base_features = (
    'gui',
)

buildsets64 = [
    {
        'os': 'windows',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features + (
            'python',
        ),
    },
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'debug',
        'features': base_features + (
            'python',
            '_nocollab',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets64,
    projects.merge_config(defprops, vs9props, x64props, ninjaprops),
    dirlen=8)

buildsets32 = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': base_features + (
            '32bit',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, paraview, buildsets32,
    projects.merge_config(defprops, vs9props, x32props, ninjaprops),
    dirlen=8)

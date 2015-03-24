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
    'test_include_labels:builderconfig': [
        'PARAVIEW',
    ],
    'test_excludes:builderconfig': [
        'UncertaintyRendering', # TODO: why?
        'pvcs-collab.CreateDelete', # TODO: why?
        'OpenHelp', # random clucene exceptions
    ],

    'slaveenv': {
        'JSDUCK_HOME': 'C:/Tools/jsduck-4.4.1',
    },
}

#------------------------------------------------------------------------------
# VS9 (2008) 64-bit properties and environment.
#------------------------------------------------------------------------------
vs9x64props = {
    'compiler': 'msvc-2008-64bit',
    'vcvarsall' : 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument' : 'amd64',

    'slaveenv': {
        'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x64/bin;C:/Tools/Python27/x64;${PATH}'
    },
}
#------------------------------------------------------------------------------
# VS9 (2008) 32-bit properties and environment.
#------------------------------------------------------------------------------
vs9x32props = {
    'compiler': 'msvc-2008-32bit',
    'vcvarsall' : 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument' : 'x86',

    'slaveenv': {
        'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x32/bin;C:/Tools/Python27/x32;${PATH}'
    },
}

#------------------------------------------------------------------------------
ninjaprops = {
    'generator': 'Ninja',
    'buildflags': '-l9',
}

#vs9Gx32props = {
#    'generator': 'Visual Studio 9 2008',
#    'buildflags': '-l9',
#}
#
#vs9Gx64props = {
#    'generator': 'Visual Studio 9 2008 Win64',
#    'buildflags': '-l9',
#}

#------------------------------------------------------------------------------
defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'VTK_LEGACY_REMOVE:BOOL': 'ON',
    'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
    'PARAVIEW_DATA_STORE:PATH': 'C:/Dashboards/data/paraview',
}

defconfigx64 = {
    'PYTHON_EXECUTABLE:FILEPATH' : 'C:/Tools/Python27/x64/python.exe',
    'PYTHON_INCLUDE_DIR:PATH' : 'C:/Tools/Python27/x64/include',
    'PYTHON_LIBRARY:FILEPATH' : 'C:/Tools/Python27/x64/libs/python27.lib',
}

defconfigx32 = {
# We don't have 32-bit Python on this machine for dashboards.
#   'PYTHON_EXECUTABLE:FILEPATH' : 'C:/Tools/Python27/x32/python.exe',
#   'PYTHON_INCLUDE_DIR:PATH' : 'C:/Tools/Python27/x32/include',
#   'PYTHON_LIBRARY:FILEPATH' : 'C:/Tools/Python27/x32/libs/python27.lib',
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
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets64,
    defprops=projects.merge_config(projects.merge_config(defprops, ninjaprops), vs9x64props),
    defconfig=projects.merge_config(defconfig, defconfigx64),
    dirlen=8
)

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

BUILDERS.extend(projects.make_builders(slave.SLAVE, paraview, buildsets32,
    defprops=projects.merge_config(projects.merge_config(defprops, ninjaprops), vs9x32props),
    defconfig=projects.merge_config(defconfig, defconfigx32),
    dirlen=8
    )
)

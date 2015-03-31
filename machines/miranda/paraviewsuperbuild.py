import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # Since server is MPI enabled, it needs to be run with MPI.
        # We'll fix that at some point.
        'PrintVersionServer',
    ],

    'configure_options:builderconfig': {
        "7Z_EXE:FILEPATH": "C:/Program Files/7-Zip/7z.exe",

        # Location of the ftjam freetype build system executable
        "FTJAM_EXECUTABLE:FILEPATH": "C:/Tools/ftjam-2.5.2/jam.exe",

        # Use system qt
        "USE_SYSTEM_qt:BOOL": "ON",

        # Package the system qt files.
        "PACKAGE_SYSTEM_QT:BOOL": "ON",

        #Location where source tar-balls are (to be) downloaded.
        "download_location:PATH":"c:/bbd/superbuild-downloads",
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
x64props = {
    'compiler': 'msvc-2008-x64',
    'vcvarsargument': 'amd64',

    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Tools/qt-4.8.4/vs2008-x64/bin/qmake.exe',

        'PYTHON_EXECUTABLE:FILEPATH': 'C:/Tools/Python27/x64/python.exe',
        'PYTHON_INCLUDE_DIR:PATH': 'C:/Tools/Python27/x64/include',
        'PYTHON_LIBRARY:FILEPATH': 'C:/Tools/Python27/x64/libs/python27.lib',
    },

    'slaveenv': {
        'PATH': 'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x64/bin;${PATH}'
    },
}

x32props = {
    'compiler': 'msvc-2008-x32',
    'vcvarsargument': 'x86',

    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Tools/qt-4.8.4/vs2008-x32/bin/qmake.exe',

        # We don't have 32-bit Python on this machine for dashboards.
        #'PYTHON_EXECUTABLE:FILEPATH': 'C:/Tools/Python27/x32/python.exe',
        #'PYTHON_INCLUDE_DIR:PATH': 'C:/Tools/Python27/x32/include',
        #'PYTHON_LIBRARY:FILEPATH': 'C:/Tools/Python27/x32/libs/python27.lib',
    },

    'slaveenv': {
        'PATH': 'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x32/bin;${PATH}'
    },
}

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave, paraviewsuperbuild, buildsets,
    projects.merge_config(defprops, vs9props, x64props),
    dirlen=8)

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild','32bit',),
    },
]

BUILDERS += projects.make_builders(slave, paraviewsuperbuild, buildsets,
    projects.merge_config(defprops, vs9props, x32props),
    dirlen=8)

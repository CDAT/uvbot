import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

BUILDERS = []

defprops = {
    'configure_options:builderconfig': {
        # Manually specify the Fortran compiler.
        'CMAKE_Fortran_COMPILER:FILEPATH': '/usr/local/bin/gfortran',
        'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',

        'download_location:PATH': '/Users/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads',

        'SUBPROJECT_GENERATOR:STRING': 'Unix Makefiles',
        'SUBPROJECT_BUILD_FLAGS:STRING': '-j5',
    },
}

osx105props = projects.merge_config(defprops, {
    'configure_options:builderconfig': {
        # Force the Python version.
        'PYTHON_EXECUTABLE:FILEPATH': '/usr/bin/python2.6',
        'PYTHON_INCLUDE_DIR:PATH': '/System/Library/Frameworks/Python.framework/Versions/2.6/Headers',
        'PYTHON_LIBRARY:FILEPATH': '/usr/lib/libpython2.6.dylib',
    },
})

osx105buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'osx10.5',
            'superbuild',

            '_webdoc',
        ),
    },
]

# temporarily disabling 10.5 superbuilds. Kamino is too busy. We can only afford
# 1 superbuild at this moment.
#BUILDERS += projects.make_builders(slave.SLAVE, paraviewsuperbuild, osx105buildsets, osx105props)

osx107props = projects.merge_config(defprops, {
    'configure_options:builderconfig': {
        # Force the Python version.
        'PYTHON_EXECUTABLE:FILEPATH': '/usr/bin/python2.7',
        'PYTHON_INCLUDE_DIR:PATH': '/System/Library/Frameworks/Python.framework/Versions/2.7/Headers',
        'PYTHON_LIBRARY:FILEPATH': '/usr/lib/libpython2.7.dylib',
    },
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

BUILDERS += projects.make_builders(slave.SLAVE, paraviewsuperbuild, osx107buildsets, osx107props)

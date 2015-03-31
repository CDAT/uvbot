from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('nemesis', secrets.SECRETS['nemesis']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Users/kitware/misc/root/cmake', # CMake 3.2.1
        'sharedresourcesroot': 'C:/Users/kitware/dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'msvc-2013-x64',

    'generator:buildslave': 'Ninja',
    'buildflags:buildslave': '-l9',

    'maximum_parallel_level': 5,

    'configure_options:buildslave': {
        'CMAKE_MAKE_PROGRAM:FILEPATH': 'C:/Users/kitware/misc/root/cmake/bin/ninja.exe',
        'CMAKE_NINJA_FORCE_RESPONSE_FILE:BOOL': 'ON', # paths are too long
    },

    'vcvarsall': 'C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat',
    'vcvarsargument': 'x64',
}

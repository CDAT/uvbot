from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('nemesis', secrets.SECRETS['nemesis']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Users/kitware/misc/root/cmake',
        'sharedresourcesroot': 'C:/Users/kitware/dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
        'compiler': 'msvc-2013-x64',

        'generator': 'Ninja',
        'buildflags': '-l9',

        'maximum_parallel_level': 5,

        'configure_options:buildslave': {
            'CMAKE_MAKE_PROGRAM:FILEPATH': 'C:/Users/kitware/misc/root/cmake/bin/ninja.exe',
            'CMAKE_NINJA_FORCE_RESPONSE_FILE:BOOL': 'ON', # paths are too long
        },

        'vcvarsall': 'C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat',
        'vcvarsargument': 'x64',
    }
)

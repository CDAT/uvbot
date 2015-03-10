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
        'compiler': 'msvc-2013',

        'generator': 'Ninja',
        'buildflags': '-l9',

        'configure_options:buildslave': {
            'CMAKE_MAKE_PROGRAM:FILEPATH': 'C:/Users/kitware/misc/root/cmake/bin/ninja.exe',
            'CMAKE_NINJA_FORCE_RESPONSE_FILE:BOOL': 'ON', # paths are too long
        },
    },
    env={
        'PATH': 'C:/Users/kitware/misc/root/cmake/bin;${PATH}',
    }
)

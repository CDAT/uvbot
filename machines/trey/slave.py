from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('trey', secrets.SECRETS['trey']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/Users/kitware/misc/root/cmake', # 3.1.3

        'os': 'osx',
        'distribution': 'osx-10.10-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'clang-apple-6.0',

    'generator:buildslave': 'Ninja',
    'buildflags:buildslave': '-l5',

    'maximum_parallel_level': 5,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

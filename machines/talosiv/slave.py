from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('talosiv', secrets.SECRETS['talosiv']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/Applications/CMake_3.1.1.app/Contents', # 3.1.1

        'os': 'osx',
        'distribution': 'osx-10.10-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'clang-apple-6.0',

    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j9 -l9',

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

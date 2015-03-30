from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('talosiv', secrets.SECRETS['talosiv']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/Applications/CMake_3.1.1.app/Contents/bin', # 3.1.1
        'sharedresourcesroot': '/Users/dashboard/Dashboards',

        'os': 'osx',
        'distribution': 'osx-10.10-x86_64',
        'compiler': 'clang-apple-6.0',

        'generator': 'Unix Makefiles',
        'buildflags': '-j9 -l9',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

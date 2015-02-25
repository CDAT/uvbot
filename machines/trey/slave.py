from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('trey', secrets.SECRETS['trey']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/Users/kitware/misc/root/cmake', # 3.1.3
        'sharedresourcesroot': '/Users/kitware/dashboards',

        'os': 'osx',
        'distribution': 'osx-10.10-x86_64',
        'compiler': 'clang-apple-6.0',

        'generator': 'Ninja',
        'buildflags': '-l5',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

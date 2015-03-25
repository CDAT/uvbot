from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('kamino', secrets.SECRETS['kamino']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/Users/kitware/Dashboards/Support/cmake-2.8.11.2', # 2.8.11.2
        'sharedresourcesroot': '/Users/kitware/Dashboards',

        'os': 'osx',
        'distribution': 'osx-10.7-x86_64',

        'generator': 'Unix Makefiles',
        'buildflags': '-j5 -l5',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('dashlin1', secrets.SECRETS['dashlin1']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/home/kitware/Dashboards/Support/cmake/install', # 2.8.11
        'sharedresourcesroot': '/home/kitware/Dashboards/MyTests',

        'os': 'linux',
        'distribution': 'ubuntu-12.04-x86_64',
        'compiler': 'gcc-4.6.3',

        'generator': 'Unix Makefiles',
        'buildflags': '-j9',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

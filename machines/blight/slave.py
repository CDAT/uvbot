from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('blight', secrets.SECRETS['blight']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/opt/apps/cmake-3.0.1',
        'sharedresourcesroot': '/home/kitware/Dashboards/MyTests',

        'os': 'linux',
        'distribution': 'ubuntu-12.04-x86_64',
        'compiler': 'gcc-4.6.3',

        'generator': 'Unix Makefiles',
        'buildflags': '-l9',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

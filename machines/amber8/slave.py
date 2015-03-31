from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('amber8', secrets.SECRETS['amber8']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/home/kitware/cmake', # 2.8.9
        'sharedresourcesroot': '/home/kitware/Dashboards/MyTests',

        'os': 'linux',
        'distribution': 'ubuntu-12.04-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.6.3',

    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j9',

    'maximum_parallel_level': 9,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

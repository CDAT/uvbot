from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('renar', secrets.SECRETS['renar']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr/local',

        'os': 'linux',
        'distribution': 'ubuntu-14.04-x86_64',
    })

SLAVEPROPS = {
    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j20',

    'maximum_parallel_level': 20,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

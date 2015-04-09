from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('garant', secrets.SECRETS['garant']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'os': 'linux',
        'distribution': 'ubuntu-14.04',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.8.2',

#    'generator:buildslave': 'Ninja',
#    'buildflags:buildslave': '-l9',

    'maximum_parallel_level': 4,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

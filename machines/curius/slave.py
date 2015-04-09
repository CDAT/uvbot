from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('curius', secrets.SECRETS['curius']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'os': 'linux',
        'distribution': 'fedora-21-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.9.2',

#    'generator:buildslave': 'Ninja',
#    'buildflags:buildslave': '-l9',

    'maximum_parallel_level': 5,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

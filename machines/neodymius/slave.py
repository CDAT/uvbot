from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('neodymius', secrets.SECRETS['neodymius']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'sharedresourcesroot': '/home/kitware/Dashboards',

        'os': 'linux',
        'distribution': 'fedora-19-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.8.3',

    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j9',

    'maximum_parallel_level': 9,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',

        'MPIEXEC:FILEPATH': 'mpiexec.hydra',
    },
}

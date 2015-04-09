from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('hythloth', secrets.SECRETS['hythloth']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/home/kitware/Dashboards/CMakeRelease-install',
        'sharedresourcesroot': '/home/kitware/Dashboards/My Tests',

        'os': 'linux',
        'distribution': 'debian-testing-x86_64',
   }
)

SLAVEPROPS = {
    'compiler': 'gcc-debian-testing',
    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j4 -l5',

    'maximum_parallel_level': 4,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

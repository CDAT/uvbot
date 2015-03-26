from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('neodymius', secrets.SECRETS['neodymius']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'sharedresourcesroot': '/home/kitware/Dashboards',

        'os': 'linux',
        'distribution': 'fedora-19-x86_64',

        'generator': 'Unix Makefiles',
        'buildflags': '-j9',

        'maximum_parallel_level': 9,

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',

            'MPIEXEC:FILEPATH': 'mpiexec.hydra',
        },
    }
)

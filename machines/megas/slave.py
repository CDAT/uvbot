from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('megas', secrets.SECRETS['megas']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'fedora-21-x86_64',
        'compiler': 'gcc-4.9.2',

        'generator': 'Ninja',
        'buildflags': '-l9',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',

            'MPIEXEC:PATH': '/usr/lib64/mpich/bin/mpiexec',
        },
    }
)

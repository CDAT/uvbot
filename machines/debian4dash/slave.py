from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('debian4dash', secrets.SECRETS['debian4dash']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr/local', # 2.8.12
        'sharedresourcesroot': '/home/kitware/Dashboards',

        'os': 'linux',
        'distribution': 'debian-4-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.1.2',

    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j3',

    'maximum_parallel_level': 3,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

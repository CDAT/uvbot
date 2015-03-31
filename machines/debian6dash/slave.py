from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('debian6dash', secrets.SECRETS['debian6dash']['password'],
    max_builds=1,
    properties={
        #'cmakeroot': '/usr', # 2.8.2
        'cmakeroot': '/home/kitware/misc/root/cmake', # 3.1.3

        'os': 'linux',
        'distribution': 'debian-6-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.4.5',

    'generator:buildslave': 'Unix Makefiles',
    'buildflags:buildslave': '-j3',

    'maximum_parallel_level': 3,

    'configure_options:buildslave': {
        'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
        'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
    },
}

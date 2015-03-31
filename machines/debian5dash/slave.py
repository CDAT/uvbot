from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('debian5dash', secrets.SECRETS['debian5dash']['password'],
    max_builds=1,
    properties={
        #'cmakeroot': '/usr', # 2.8.2
        'cmakeroot': '/home/kitware/misc/root/cmake', # 3.1.3
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'debian-5-x86_64',
        'compiler': 'gcc-4.4.5',

        'generator:buildslave': 'Unix Makefiles',
        'buildflags:buildslave': '-j3',

        'maximum_parallel_level': 3,

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

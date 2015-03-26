from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('debian6dash', secrets.SECRETS['debian6dash']['password'],
    max_builds=1,
    properties={
        #'cmakeroot': '/home/kitware/misc/root/cmake', # 3.1.3
        'cmakeroot': '/usr', # 2.8.9
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'debian-7-x86_64',
        'compiler': 'gcc-4.7.2',

        'generator': 'Unix Makefiles',
        'buildflags': '-j3',

        'maximum_parallel_level': 3,

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

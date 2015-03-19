from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('debian4dash', secrets.SECRETS['debian4dash']['password'],
    max_builds=1,
    properties={
        #'cmakeroot': '/usr', # 2.8.2
        'cmakeroot': '/home/kitware/misc/root/cmake', # 3.1.3
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'debian-4-x86_64',
        'compiler': 'gcc-4.1.2',

        'generator': 'Unix Makefiles',
        'buildflags': '-j3',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    },
    env={
        'PATH': '/home/kitware/Dashboards/support/git/bin:${PATH}',
    }
)

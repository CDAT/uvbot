from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('tarvalon', secrets.SECRETS['tarvalon']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Program Files (x86)/CMake 2.8', # 2.8.7
        'sharedresourcesroot': 'C:/Dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
        'compiler': 'msvc-2010',

        'generator': 'Visual Studio 2010',
        'buildflags': '',

        'configure_options:buildslave': {},
    }
)

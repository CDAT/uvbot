from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('tarvalon', secrets.SECRETS['tarvalon']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Users/dashboard/cmake-3.1.3', # 3.1.3
        'sharedresourcesroot': 'C:/Dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
        'compiler': 'msvc-2010',

        'generator': 'Visual Studio 10 Win64',
        'buildflags': '',

        'configure_options:buildslave': {},
    }
)

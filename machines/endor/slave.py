from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('endor', secrets.SECRETS['endor']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr/local', # 2.8.12.2
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'ubuntu-12.04-x86_64',
        'compiler': 'gcc-4.6.3',

        'generator:buildslave': 'Unix Makefiles',
        'buildflags:buildslave': '-j9 -l9',
    }
)

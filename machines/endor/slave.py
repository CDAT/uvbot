from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('endor', secrets.SECRETS['endor']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'sharedresourcesroot': '/home/kitware/dashboards',

        'os': 'linux',
        'distribution': 'ubuntu-12.04-x86_64',
        'compiler': 'gcc-4.6.3',

        'generator': 'Unix Makefiles',
        'buildflags': '-j9 -l9',
    }
)

from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('nemesis', secrets.SECRETS['nemesis']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'sharedresourcesroot': 'C:/Users/kitware/dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
        'compiler': 'msvc-2013',

        'generator': 'Ninja',
        'buildflags': '-l9',

        'configure_options:buildslave': {
        },
    }
)

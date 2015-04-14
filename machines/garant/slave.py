from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('garant', secrets.SECRETS['garant']['password'],
    max_builds=2,
    properties={
        'cmakeroot': '/usr',
        'os': 'linux',
        'distribution': 'ubuntu-14.04',
        'selenium': '8101'
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.8.2',
    'generator:buildslave': 'Unix Makefiles',
    'maximum_parallel_level': 4,
    'configure_options:buildslave': {},
}

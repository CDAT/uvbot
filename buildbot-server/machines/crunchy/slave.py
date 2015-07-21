from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('crunchy', secrets.SECRETS['crunchy']['password'],
    max_builds=2,
    properties={
        'cmakeroot': '/usr/local',
        'os': 'linux',
        'distribution': 'redhat-6',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.4.7',
    'generator:buildslave': 'Unix Makefiles',
    'maximum_parallel_level': 8,
    'configure_options:buildslave': {}
}

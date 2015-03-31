from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('tarvalon', secrets.SECRETS['tarvalon']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Support/cmake-3.2.1-win32-x86', # 3.2.1

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
    })

SLAVEPROPS = {
    'compiler': 'msvc-2010-x64',

    'generator:buildslave': 'Visual Studio 10 Win64',
    'buildflags:buildslave': '',

    'maximum_parallel_level': 5,

    'configure_options:buildslave': {},
}

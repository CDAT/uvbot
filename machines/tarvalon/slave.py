from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('tarvalon', secrets.SECRETS['tarvalon']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Support/cmake-3.2.1-win32-x86', # 3.2.1
        'sharedresourcesroot': 'C:/Dashboards',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',
        'compiler': 'msvc-2010-x64',

        'generator': 'Visual Studio 10 Win64',
        'buildflags': '',

        'configure_options:buildslave': {},
    }
)

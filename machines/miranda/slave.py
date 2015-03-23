from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('miranda', secrets.SECRETS['miranda']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Tools/cmake-3.2.1-x64',
        'sharedresourcesroot': 'C:/Dashboards/MyTests',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',

        'configure_options:buildslave': {
            'CMAKE_MAKE_PROGRAM:FILEPATH': 'C:/Tools/Ninja/ninja/ninja.exe',
            'CMAKE_NINJA_FORCE_RESPONSE_FILE:BOOL': 'ON', # paths are too long
        },
    }
)

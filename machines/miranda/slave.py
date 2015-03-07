from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('miranda', secrets.SECRETS['miranda']['password'],
    max_builds=1,
    properties={
        'cmakeroot': 'C:/Program Files (x86)/CMake 2.8',
        'sharedresourcesroot': 'C:/Dashboards/MyTests',

        'os': 'windows',
        'distribution': 'windows-7-x86_64',

        # set the default compiler and environment.
        'compiler': 'msvc-2008-64bit',
        'vcvarsall' : 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
        'vcvarsargument' : 'amd64',

        'configure_options:buildslave': {
            'CMAKE_MAKE_PROGRAM:FILEPATH': 'C:/Tools/Ninja/ninja/ninja.exe',
            'CMAKE_NINJA_FORCE_RESPONSE_FILE:BOOL': 'ON', # paths are too long
        },
    }
)

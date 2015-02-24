from buildbot.buildslave import BuildSlave

__all__ = [
    'SLAVE',
]

SLAVE = BuildSlave('trey', 'XXXXXXXX',
    max_builds=1,
    properties={
        'cmakeroot': '/Users/kitware/misc/root/cmake', # 3.1.3
        'sharedresourcesroot': '/Users/kitware/dashboards',

        'os': 'osx',
        'distribution': 'osx-10.10-x86_64',
        'compiler': 'clang-apple-6.0',
        'generator': 'Ninja',

        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },
    }
)

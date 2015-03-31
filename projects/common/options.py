os = {
    'linux': {},
    'osx': {
        'configure_options:project': {
            # CMake is picking make -i as default, which ends up ignoring
            # errors and wasting time!
            'MAKE_COMMAND:STRING': '/usr/bin/make',
        },
    },
    'windows': {},
}
libtypes = {
    'shared': {
        'configure_options:project': {
            'BUILD_SHARED_LIBS:BOOL': 'ON',
        },
    },
    'static': {
        'configure_options:project': {
            'BUILD_SHARED_LIBS:BOOL': 'OFF',
        },
    },
}
buildtypes = {
    'release': {
        'configure_options:project': {
            'CMAKE_BUILD_TYPE:STRING': 'Release',
        },
    },
    'debug': {
        'configure_options:project': {
            'CMAKE_BUILD_TYPE:STRING': 'Debug',
        },
    },
    'relwithdebinfo': {
        'configure_options:project': {
            'CMAKE_BUILD_TYPE:STRING': 'RelWithDebInfo',
        },
    },
}

categories = {
    'expected': {},
    'exotic': {},
    'experimental': {},

    'default' : 'expected',
}

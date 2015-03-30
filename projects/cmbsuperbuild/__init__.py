__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'cmb'

DEFAULTS = {
    'generator': 'Unix Makefiles',
    'buildflags': '-j1',

    'upload_file_patterns:project': [
        '*.tar.gz',
        '*.tgz',
    ],

    'configure_options:project': {
        'BUILD_TESTING:BOOL': 'ON',

        'ENABLE_cmb_BUILD_MODE:STRING': 'SuperBuild',
    },

    'cdash_url': 'https://www.kitware.com/CDash',
    'cdash_project': 'CMB',
}

OPTIONS = {
    'os': {
        'linux': {},
        'windows': {
            'upload_file_patterns:project': [
                '*.zip',
                '*.exe',
            ],

            'generator': 'Ninja',
        },
        'osx': {
            'upload_file_patterns:project': [
                '*.dmg',
            ],

            # CMake is picking make -i as default, which ends up ignoring errors and wasting time!
            'MAKE_COMMAND:STRING': '/usr/bin/make',
        },
    },
    'libtype': {
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
    },
    'buildtype': {
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
    },
    'category': {
        'expected': {},
        'exotic': {},
        'experimental': {},
        'default' : 'expected',
    },
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
    'superbuild': ({}, {}),
}

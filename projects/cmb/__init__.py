__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'cmb'

DEFAULTS = {
    'cdash_url': 'https://www.kitware.com/CDash',
    'cdash_project': 'CMB',
}

OPTIONS = {
    'os': {
        'linux': {},
        'windows': {},
        'osx': {},
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
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {}

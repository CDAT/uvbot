__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'paraview'

DEFAULTS = {
    'test_include_labels:project': [
        'PARAVIEW',
    ],
    'configure_options:project': {
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
    },

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'ParaView',
}

OPTIONS = {
    'os': {
        'linux': {},
        'osx': {},
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
    },
    'category': {
        'expected': {},
        'exotic': {},
        'experimental': {},
        'default' : 'expected',
    },
}

OPTIONORDER = ('os', 'buildtype',)

FEATURES = {
    'catalyst': ({}, {}),
}

from projects.common import options

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
    'buildtype': options.buildtypes,
    'category': options.categories,
}

OPTIONORDER = ('os', 'buildtype',)

FEATURES = {
    'catalyst': ({}, {}),
}

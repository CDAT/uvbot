import projects
from projects.common import features
from projects.common import options

__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'geojs'

DEFAULTS = {
    'configure_options:project': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'BUILD_TESTING:BOOL': 'ON',
    },
    'cdash_url': 'https://my.cdash.org',
    'cdash_project': 'geojs',
}

OPTIONS = {
    'os': options.os
}
OPTIONORDER = ('os', )

FEATURES = {
    'selenium': projects.make_feature_cmake_options({
        'SELENIUM_TESTS:BOOL': ('OFF', 'ON')
    }),
    'chrome': projects.make_feature_cmake_options({
        'CHROME_TESTS:BOOL': ('OFF', 'ON')
    }),
    '_noexamples': ({}, {
        'configure_options:feature': {
            'BUILD_EXAMPLES:BOOL': 'OFF',
        },
    }),
}

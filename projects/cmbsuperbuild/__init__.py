import projects
from projects.common import options
from projects.common import superbuild

__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'cmb'

DEFAULTS = projects.merge_config(superbuild.defaults, {
    'configure_options:project': {
        'BUILD_TESTING:BOOL': 'ON',

        'ENABLE_cmb_BUILD_MODE:STRING': 'SuperBuild',
    },

    'cdash_url': 'https://www.kitware.com/CDash',
    'cdash_project': 'CMB',
})

OPTIONS = {
    'os': superbuild.os,
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
    'category': options.categories,
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
    'superbuild': ({}, {}),
}

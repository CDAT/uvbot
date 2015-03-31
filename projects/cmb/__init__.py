from projects.common import features
from projects.common import options

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
    'os': options.os,
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
    '_strict': features.strict,
}

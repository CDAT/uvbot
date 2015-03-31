import projects
from projects.common import features
from projects.common import options
from projects.common import superbuild

__all__ = [
    'NAME',
    'DEFAULTS',
    'OPTIONS',
    'OPTIONORDER',
    'FEATURES',
]

NAME = 'vtk'

DEFAULTS = projects.merge_config(superbuild.defaults, {
    'configure_options:project': {
        'BUILD_TESTING:BOOL': 'ON',
        'ENABLE_vtk:BOOL': 'ON',
        "GENERATE_JAVA_PACKAGE:BOOL": "ON",
    },

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'VTK',
})

OPTIONS = {
    'os': superbuild.os,
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
}

OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': ({}, {}),
    'osx10.5': features.osx105,
    'osx10.7': features.osx107,
    '32bit': ({}, {}),
}

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

NAME = 'paraview'

DEFAULTS = projects.merge_config(superbuild.defaults, {
    'configure_options:project': {
        'BUILD_TESTING:BOOL': 'ON',

        'USE_NONFREE_COMPONENTS:BOOL': 'ON',

        'ENABLE_acusolve:BOOL': 'ON',
        'ENABLE_boost:BOOL': 'ON',
        'ENABLE_cgns:BOOL': 'ON',
        'ENABLE_cosmotools:BOOL': 'ON',
        'ENABLE_ffmpeg:BOOL': 'ON',
        'ENABLE_manta:BOOL': 'ON',
        'ENABLE_matplotlib:BOOL': 'ON',
        'ENABLE_mpi:BOOL': 'ON',
        'ENABLE_nektarreader:BOOL': 'ON',
        'ENABLE_netcdf:BOOL': 'ON',
        'ENABLE_numpy:BOOL': 'ON',
        'ENABLE_paraview:BOOL': 'ON',
        'ENABLE_python:BOOL': 'ON',
        'ENABLE_qt:BOOL': 'ON',
        'ENABLE_silo:BOOL': 'ON',
        'ENABLE_visitbridge:BOOL': 'ON',
        'ENABLE_vistrails:BOOL': 'ON',
    },

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'ParaView',
})

OPTIONS = {
    'os': projects.merge_config(superbuild.os, {
        'windows': {
            'configure_options:project': {
                'ENABLE_cosmotools:BOOL': 'OFF',
                'ENABLE_manta:BOOL': 'OFF',
                'ENABLE_nektarreader:BOOL': 'OFF',
            },
        },
        'osx': {
            'test_excludes:project': [
                # QtTesting has some issue with playback/capture for this
                # one on OsX. We'll fix it at some point
                'TestPythonView',
            ],

            'configure_options:project': {
                # Manta is not supported on OS X in our superbuild.
                'ENABLE_manta:BOOL': 'OFF',
            },
        },
    }),
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
    'category': options.categories,
}
OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': ({}, {}),
    'osx10.5': features.osx105,
    'osx10.7': features.osx107,
    '32bit': ({}, {}),

    '_webdoc': ({}, {
        'configure_options:feature': {
            'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',
        },
    }),
}

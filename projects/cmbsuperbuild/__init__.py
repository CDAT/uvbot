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
    'libtype': options.libtypes,
    'buildtype': options.buildtypes,
    'category': options.categories,
}
OPTIONORDER = ('os', 'libtype', 'buildtype',)

FEATURES = {
    'superbuild': ({}, {}),
}

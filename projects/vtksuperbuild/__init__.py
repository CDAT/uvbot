__all__ = [
    'NAME',
    'DEFAULTS',
    'OPTIONS',
    'OPTIONORDER',
    'FEATURES',
]

NAME = 'vtksuperbuild'

DEFAULTS = {
    'generator': 'Unix Makefiles',
    'buildflags': '-j1',

    'upload_file_patterns:project': [
        '*.tar.gz',
        '*.tgz',
    ],

    'configure_options:project': {
        'BUILD_TESTING:BOOL': 'ON',
        'ENABLE_vtk:BOOL': 'ON',
        "GENERATE_JAVA_PACKAGE:BOOL": "ON",
    },
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
            'BUILD_SHARED_LIBS:BOOL': 'ON',
        },
    },
    'buildtype': {
        'release': {
            'CMAKE_BUILD_TYPE:STRING': 'Release',
        },
    },
}

OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': {},
    'osx10.7': {},
    '32bit': {},
    '64bit': {},
}

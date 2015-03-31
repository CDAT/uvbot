from projects.common import options

__all__ = [
    'NAME',
    'DEFAULTS',
    'OPTIONS',
    'OPTIONORDER',
    'FEATURES',
]

NAME = 'vtk'

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

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'VTK',
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
}

OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': ({}, {}),
    'osx10.5': ({}, {
        'configure_options:feature': {
            'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.6.sdk',
            'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',
            'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.5',

        },
    }),
    'osx10.7': ({}, {
        'configure_options:feature': {
            'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
            'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',
            'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.7',
        },
    }),
    '32bit': ({}, {}),
    '64bit': ({}, {}),
}

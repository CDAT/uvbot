__all__ = [
    'NAME',

    'DEFAULTS',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'paraview'

DEFAULTS = {
    'generator': 'Unix Makefiles',
    'buildflags': '-j1',

    'upload_file_patterns:project': [
        '*.tar.gz',
        '*.tgz',
    ],

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
}

OPTIONS = {
    'os': {
        'linux': {},
        'windows': {
            'upload_file_patterns:project': [
                '*.zip',
                '*.exe',
            ],

            'configure_options:project': {
                'ENABLE_cosmotools:BOOL': 'OFF',
                'ENABLE_manta:BOOL': 'OFF',
                'ENABLE_nektarreader:BOOL': 'OFF',
            },

            'generator': 'Ninja',
        },
        'osx': {
            'test_excludes:project': [
                # QtTesting has some issue with playback/capture for this
                # one on OsX. We'll fix it at some point
                'TestPythonView',
            ],

            'upload_file_patterns:project': [
                '*.dmg',
            ],

            'configure_options:project': {
                # Manta is not supported on OsX in our superbuild.
                'ENABLE_manta:BOOL': 'OFF',
            },

            # CMake is picking make -i as default, which ends up ignoring errors and wasting time!
            'MAKE_COMMAND:STRING': '/usr/bin/make',
        },
    },
    'libtype': {
        'shared': {
            'configure_options:project': {
                'BUILD_SHARED_LIBS:BOOL': 'ON',
            },
        },
        'static': {
            'configure_options:project': {
                'BUILD_SHARED_LIBS:BOOL': 'OFF',
            },
        },
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
OPTIONORDER = ('os', 'libtype', 'buildtype')

FEATURES = {
    'superbuild': ({}, {}),
    'osx10.5': ({}, {
        'configure_options:feature': {
            'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.6.sdk',
            'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.5',
        },
    }),
    'osx10.7': ({}, {
        'configure_options:feature': {
            'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
            'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.7',
        },
    }),
    '32bit': ({}, {}),

    '_webdoc': ({}, {
        'configure_options:feature': {
            'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',
        },
    }),
}

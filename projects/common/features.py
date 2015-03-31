# Visual Studio
vs = ({}, {
    'configure_options:feature': {
        'CMAKE_CXX_MP_FLAG:BOOL': 'ON',
    },
})

# OS X
osx105 = ({}, {
    'configure_options:feature': {
        'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.6.sdk',
        'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.5',
    },
})
osx107 = ({}, {
    'configure_options:feature': {
        'CMAKE_OSX_SYSROOT:PATH': '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk',
        'CMAKE_OSX_DEPLOYMENT_TARGET:STRING': '10.7',
    },
})

# Compilers
icc = ({}, {
    'slaveenv': {
        'CC': 'icc',
        'CXX': 'icpc',
    },
})
clang = ({}, {
    'slaveenv': {
        'CC': 'clang',
        'CXX': 'clang++',
    },
})

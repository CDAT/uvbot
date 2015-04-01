import random

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

strict = ({}, {
    'slaveenv': {
        # glibc: https://udrepper.livejournal.com/11429.html
        #        http://www.novell.com/support/kb/doc.php?id=3113982
        #        http://bitwagon.com/glibc-memlap/glibc-memlap.html
        'MALLOC_PERTURB_': str(random.randint(1, 255)),
        'MALLOC_CHECK_': '3',
        'MEMCPY_CHECK_': '1',

        # OS X: http://blog.timac.org/?tag=libmallocdebug
        'MallocCheckHeapAbort': '1',
        'MallocCheckHeapEach': '1000000',
        'MallocCheckHeapStart': '1',
        'MallocErrorAbort': '1',
        'MallocGuardEdges': '1',
        'MallocLogFile': '/dev/null',
        'MallocPreScribble': '1',
        'MallocScribble': '1',
        'NSZombieEnabled': 'YES',
    },
})

parallel = ({}, {
    'supports_parallel_testing:feature': True,
    },
)

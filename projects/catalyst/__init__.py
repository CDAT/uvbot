
__all__ = [
    'NAME',

    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'paraview'

OPTIONS = {
    'os': {
        'linux': {},
        'osx': {},
    },
    'buildtype': {
        'release': {
            'CMAKE_BUILD_TYPE:STRING': 'Release',
        },
        'debug': {
            'CMAKE_BUILD_TYPE:STRING': 'Debug',
        },
    },
}

OPTIONORDER = ('os', 'buildtype',)

FEATURES = {
    'catalyst': {},
}

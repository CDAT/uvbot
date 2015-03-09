import projects
from projects import catalyst

__all__ = [
    'BUILDERS',
]

defprops = {}

defconfig = {}

env = {
    'DISPLAY': ':1',
}

buildsets = [
    {
        'os': 'linux',
        'features' : ('catalyst',),
    },
]

BUILDERS = projects.make_builders(catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['megas'],
    env=env
)

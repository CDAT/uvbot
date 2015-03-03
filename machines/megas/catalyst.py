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
        'editionset' : 'Base',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Essentials',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Essentials+Extras',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Essentials+Extras+Rendering-Base',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Enable-Python',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Enable-Python+Essentials',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Enable-Python+Essentials+Extras',
    },
    {
        'os': 'linux',
        'editionset' : 'Base+Enable-Python+Essentials+Extras+Rendering-Base+Rendering-Base-Python',
    },
]

BUILDERS = catalyst.make_builders(catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['megas'],
    env=env
)

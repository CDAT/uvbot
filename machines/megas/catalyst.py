import projects
from projects import catalyst

__all__ = [
    'BUILDERS',
]

defprops = {
    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',
}

defconfig = {}

env = {
    'DISPLAY': ':1',
}

buildsets = [
    {
        'os': 'linux',
    },
]

BUILDERS = projects.make_builders(catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['megas'],
    env=env
)

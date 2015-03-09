import projects
from projects import catalyst
from kwextensions import factory

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
        'features' : ('catalyst',),
    },
]

BUILDERS = projects.make_builders(catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    myfactory=factory.get_catalyst_buildfactory(),
    slavenames=['megas'],
    env=env
)

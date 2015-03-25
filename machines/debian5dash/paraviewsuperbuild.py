import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'download_location:PATH': '/home/kitware/dashboards/downloads/paraview',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets, defprops)

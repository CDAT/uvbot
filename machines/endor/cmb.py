import projects
from projects import cmb
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_initial_cache': '/home/kitware/dashboards/data/cmb/developer/cmb-Developer-Config.cmake',

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'relwithdebinfo',
        'features': (),
    },
]

BUILDERS = projects.make_builders(slave, cmb, buildsets, defprops)

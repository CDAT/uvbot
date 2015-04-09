import projects
from projects import cmb
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_initial_cache': '/Users/dashboard/Dashboards/data/cmb/developer/cmb-Developer-Config.cmake',
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (),
    },
]

BUILDERS = projects.make_builders(slave, cmb, buildsets, defprops)

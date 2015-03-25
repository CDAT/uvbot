import projects
from projects import cmb
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        #'ctest_local_extra_options_file:FILEPATH': '/Users/dashboard/Dashboards/projects/cmb/developer/cmb-Developer-Config.cmake',
    },
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, cmb, buildsets, defprops)

import projects
from projects import cmb
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        #'ctest_local_extra_options_file:FILEPATH': '/home/kitware/dashboards/projects/cmb/developer/cmb-Developer-Config.cmake',
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

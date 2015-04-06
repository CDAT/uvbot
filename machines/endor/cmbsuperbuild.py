import projects
from projects import cmbsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'developer_install_root': '/home/kitware/dashboards/data/cmb/developer',

    'configure_options:builderconfig': {
        'ENABLE_hdf5:BOOL': 'ON',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'relwithdebinfo',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave, cmbsuperbuild, buildsets, defprops)

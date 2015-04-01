import projects
from projects import cmbsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
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

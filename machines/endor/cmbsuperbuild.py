import projects
from projects import cmbsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'ENABLE_hdf5:BOOL': 'ON',
        'USE_SYSTEM_qt:BOOL': 'ON',
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

BUILDERS = projects.make_builders(slave, cmbsuperbuild, buildsets, defprops)

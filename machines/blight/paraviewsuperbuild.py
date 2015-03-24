import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'download_location:PATH': '/home/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads',
    },

    'slaveenv': {
        'DISPLAY': ':0',
        # since we're using mesa, no need to do offscreen screenshots.
        'PV_NO_OFFSCREEN_SCREENSHOTS': '1',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'superbuild',

            '_webdoc',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets, defprops)

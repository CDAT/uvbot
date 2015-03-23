import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'upload_file_patterns:builderconfig': [
        '*.tar.gz',
        '*.tgz',
    ],
    'test_excludes:builderconfig': [
        # QtTesting has some issue with playback/capture for this
        # one. We'll fix it at some point
        'TestPythonView',
    ],
}

defconfig = {
    # SVN is too old.
    'DIY_SKIP_SVN:BOOL': 'ON',

    'USE_NONFREE_COMPONENTS:BOOL': 'ON',

    'ENABLE_acusolve:BOOL': 'ON',
    'ENABLE_boost:BOOL': 'ON',
    'ENABLE_cgns:BOOL': 'ON',
    'ENABLE_cosmotools:BOOL': 'ON',
    'ENABLE_ffmpeg:BOOL': 'ON',
    'ENABLE_manta:BOOL': 'ON',
    'ENABLE_matplotlib:BOOL': 'ON',
    'ENABLE_mpi:BOOL': 'ON',
    'ENABLE_netcdf:BOOL': 'ON',
    'ENABLE_numpy:BOOL': 'ON',
    'ENABLE_paraview:BOOL': 'ON',
    'ENABLE_python:BOOL': 'ON',
    'ENABLE_qt:BOOL': 'ON',
    'ENABLE_silo:BOOL': 'ON',
    'ENABLE_visitbridge:BOOL': 'ON',
    'ENABLE_vistrails:BOOL': 'ON',

    'download_location:PATH': '/home/kitware/Dashboards/downloads/paraview',
}
env = {
    'PATH': '/home/kitware/Dashboards/support/git/bin:${PATH}',
    'DISPLAY': ':0',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    env=env
)

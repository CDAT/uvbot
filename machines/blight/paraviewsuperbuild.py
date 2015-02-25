import projects
from projects import paraviewsuperbuild

__all__ = [
    'BUILDERS',
]

defprops = {
    'upload_file_patterns:builderconfig': [
        '*.tar.gz',
        '*.tgz',
    ],
}

defconfig = {
    'USE_NONFREE_COMPONENTS:BOOL': 'ON',
    'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

    'ENABLE_acusolve:BOOL': 'ON',
    'ENABLE_boost:BOOL': 'ON',
    'ENABLE_cgns:BOOL': 'ON',
    'ENABLE_cosmotools:BOOL': 'ON',
    'ENABLE_ffmpeg:BOOL': 'ON',
    'ENABLE_manta:BOOL': 'ON',
    'ENABLE_matplotlib:BOOL': 'ON',
    'ENABLE_mpi:BOOL': 'ON',
    'ENABLE_nektarreader:BOOL': 'ON',
    'ENABLE_numpy:BOOL': 'ON',
    'ENABLE_paraview:BOOL': 'ON',
    'ENABLE_python:BOOL': 'ON',
    'ENABLE_qt:BOOL': 'ON',
    'ENABLE_silo:BOOL': 'ON',
    'ENABLE_visitbridge:BOOL': 'ON',
    'ENABLE_vistrails:BOOL': 'ON',

    'download_location:PATH': '/home/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(paraviewsuperbuild, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    slavenames=['blight']
)

import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # TODO: Why are these disabled?
        'TestTilingCxx',
        'TestInteractorStyleTreeMapHover',
        'TestStructuredGridLIC2DXSlice',
        'TestStructuredGridLIC2DYSlice',
        'TestStructuredGridLIC2DZSlice',
        'TestShadowMapPass',
        'ProjectedTetrahedraZoomIn',
        'TestHAVSVolumeMapper',
        'TestProjectedTetrahedra',
        'RenderView',
        'vtkRenderingVolumeCxx-TestGPURayCastFourComponentsMIP',
        'vtkRenderingVolumeCxx-TestGPURayCastFourComponentsMinIP',
        'vtkRenderingCoreCxx-TestEdgeFlags',
    ],

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': 'C:/Dashboards/CDashHome/ExternalData',
    },

    'slaveenv': {
        'PATH': 'C:/Support/Qt/4.8.0-vs2010-x64/bin;C:/Python27x64;${PATH}',
    },
}

buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'category': 'experimental',
        'features': (
            'mpi',
            'qt',
            'vs',

            '_noexamples',
            '_parallel',
        ),
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)

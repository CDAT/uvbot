import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # TODO: Most of these are probably Mesa problems.
        'vtkDomainsChemistryCxx-TestMoleculeSelection',
        'vtkFiltersGeneralCxx-BoxClipTetrahedra',
        'vtkInteractionWidgetsCxx-TestLogoWidgetDepthPeeling',
        'vtkRenderingOpenGLCxx-TestBlurAndSobelPasses',
        'vtkRenderingCoreCxx-TestGlyph3DMapperPicking',
        'vtkRenderingCoreCxx-TestOpacity',
        'vtkRenderingCoreCxx-TestBlockOpacity',
        'vtkRenderingCoreCxx-TestPointSelection',
        'vtkRenderingCoreCxx-TestPolygonSelection',
        'vtkRenderingFreeTypeCxx-TestTextActor3DDepthPeeling',
        'vtkRenderingCoreCxx-TestTranslucentLUTDepthPeeling',
        'vtkRenderingCoreCxx-TestTranslucentLUTTextureDepthPeeling',
        'vtkRenderingCoreCxx-TestTextureRGBADepthPeeling',
        'vtkRenderingVolumeCxx-TestProjectedTetrahedra',
        'vtkRenderingCoreCxx-TestTranslucentImageActorDepthPeeling',
        'vtkRenderingVolumeCxx-TestProp3DFollower',
        'vtkViewsInfovisCxx-TestRenderView',

        'vtkChartsCorePython-TestParallelCoordinatesColors',
        'vtkFiltersProgrammablePython-progGlyphsBySource',
        'vtkRenderingCorePython-TestOpacity2',
        'vtkRenderingCorePython-TestOpacityVectors',
        'vtkRenderingCorePython-TestWindowToImageTransparency',
        'vtkRenderingVolumePython-volTM3DCompressedCropRegions',
        'vtkRenderingVolumePython-volTM3DCropRegions',
        'vtkRenderingVolumePython-volTM3DRotateClip',
    ],

    'configure_options:builderconfig': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'BUILD_TESTING:BOOL': 'ON',
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData',
        'VTK_USER_LARGE_DATA:BOOL': 'ON',

        'Module_vtkIOXdmf2:BOOL': 'ON',
        'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
    },

    'slaveenv': {
        'DISPLAY': ':1',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'mpi',
            'python',
            'qt',
        ),
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)

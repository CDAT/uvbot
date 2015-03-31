import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_excludes:builderconfig': [
        # excluded in nightly build because:
        # Mesa Gallium swrast driver not rendering vtkContourWidget when
        # vtkImageMapToWindowLevelColors runs on the background image.
        'vtkInteractionWidgetsCxx-TestDijkstraImageGeodesicPath',
        'vtkInteractionWidgetsCxx-TestImageActorContourWidget',
    ],

    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/home/buildbot/data/vtk',

        # Java
        'Java_JAR_EXECUTABLE:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/bin/jar',
        'Java_JAVAC_EXECUTABLE:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/bin/javac',
        'Java_JAVADOC_EXECUTABLE:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/bin/javadoc',
        'Java_JAVAH_EXECUTABLE:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/bin/javah',
        'Java_JAVA_EXECUTABLE:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/bin/java',
        'JAVA_AWT_INCLUDE_PATH:PATH': '/usr/lib/jvm/java-7-openjdk-amd64/include',
        'JAVA_AWT_LIBRARY:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/libawt.so;/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/libjawt.so',
        'JAVA_INCLUDE_PATH:PATH': '/usr/lib/jvm/java-7-openjdk-amd64/include',
        'JAVA_INCLUDE_PATH2:PATH': '/usr/lib/jvm/java-7-openjdk-amd64/include/linux',
        'JAVA_JVM_LIBRARY:FILEPATH': '/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so',
        'VTK_JAVA_SOURCE_VERSION:STRING': '1.7',
        'VTK_JAVA_TARGET_VERSION:STRING': '1.7',

        # Mesa
        'OPENGL_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Mesa-install/include',
        'OPENGL_gl_LIBRARY:FILEPATH': '/home/kitware/Dashboards/Mesa-install/lib/libMesaGL.so',
        'OPENGL_glu_LIBARARY:FILEPATH': ''
        'OSMESA_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Mesa-install/include',
        'OSMESA_LIBRARY:FILEPATH': '/home/kitware/Dashboards/Mesa-install/lib/libMesaOSMesa.so',

        # Valgrind
        'PURIFYCOMMAND:FILEPATH': '/usr/bin/valgrind --leak-check=yes -v',

        # TCL/TK
        'TCL_LIBRARY:FILEPATH': '/usr/lib/x86_64-linux-gnu/libtcl8.6.so',
        'TK_LIBARARY:FILEPATH': '/usr/lib/x86_64-linux-gnu/libtk8.6.so',
        'TCL_INCLUDE_PATH:PATH': '/usr/include/tcl8.6',
        'TK_INCLUDE_PATH:PATH': '/usr/include/tcl8.6',

        # VTK
        'VTK_BUILD_ALL_MODULES:BOOL': 'ON',
# Turning this off until we find a way around the mpirun issues that is more general
# than the script given for mpirun executable.  It only works for the path of the
# nightly builds anyway.
#        'VTK_MPIRUN_EXE:FILEPATH': '/home/kitware/Dashboards/DashboardScripts/hyloth_vtk_gcc_mpirun.sh',
        'VTK_OPENGL_HAS_OSMESA:BOOL': 'OFF',
        'VTK_USE_64BIT_IDS:BOOL': 'ON',
        'VTK_USE_ANSI_STDLIB:BOOL': 'ON',
        'Module_vtkFiltersStatisticsGnuR:BOOL': 'ON',
        'VTK_TEST_TIMEOUT_TerrainPolylineEditor:STRING': '180',
        'VTK_TEST_TIMEOUT_TestPickingManagerSeedWidget:STRING': '150',
        'VTK_TEST_TIMEOUT_TestProp3DFollower:STRING': '150',
        'VTK_TEST_TIMEOUT_TestTM3DLightComponents:STRING': '150',

    },

    'referencedir': '/home/buildbot/buildbot-share/vtk',

    'slaveenv': {
        'DISPLAY': ':40',
        'CC': 'gcc',
        'CXX': 'g++',
        'LD_LIBRARY_PATH': '/home/kitware/Dashboards/Mesa-install/lib:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/xawt:${LD_LIBRARY_PATH}',
    },
}

# these are implied by all modules anyways
base_features = (
    'python',
    'qt',
    'tcl',
    'mpi',
    'java',
)
buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'category': 'experimental',
        'features': base_features,
    },
]

BUILDERS = projects.make_builders(slave, vtk, buildsets, defprops)

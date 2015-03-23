import projects
from projects import vtksuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'upload_file_patterns:builderconfig': [ '*.zip', '*.exe' ],
    'generator': 'Ninja',
    'buildflags': '-l1',
    'test_excludes:builderconfig': [
        # Since server is MPI enabled, it needs to be run with MPI.
        # We'll fix that at some point.
        'PrintVersionServer',
    ],
}

defconfig = {
    'BUILD_TESTING:BOOL': 'OFF',

    # Superbuild Variables
    "ENABLE_vtk:BOOL": "ON",
    "GENERATE_JAVA_PACKAGE:BOOL": "ON",
    "JAVA_AWT_INCLUDE_PATH:PATH": "${JDK_HOME}/include",
    "JAVA_INCLUDE_PATH:PATH": "${JDK_HOME}/include",
    "JAVA_INCLUDE_PATH2:PATH": "${JDK_HOME}/include/win32",
    "JAVA_JVM_LIBRARY:PATH": "${JDK_HOME}/lib/jvm.lib",
    "JAVA_AWT_LIBRARY:PATH": "${JDK_HOME}/lib/jawt.lib",
    "Java_JAR_EXECUTABLE:FILEPATH": "${JDK_HOME}/bin/jar.exe",
    "Java_JAVAC_EXECUTABLE:FILEPATH": "${JDK_HOME}/bin/javac.exe",
    "Java_JAVADOC_EXECUTABLE:FILEPATH": "${JDK_HOME}/bin/javadoc.exe",
    "Java_JAVAH_EXECUTABLE:FILEPATH": "${JDK_HOME}/bin/javah.exe",
    "Java_JAVA_EXECUTABLE:FILEPATH": "${JDK_HOME}/bin/java.exe",
    "JOGL_GLUE:FILEPATH": "${M2_REPO}/org/jogamp/gluegen/gluegen-rt/2.0.2/gluegen-rt-2.0.2.jar",
    "JOGL_LIB:FILEPATH": "${M2_REPO}/org/jogamp/jogl/jogl-all/2.0.2/jogl-all-2.0.2.jar",

    "7Z_EXE:FILEPATH": "C:/Program Files/7-Zip/7z.exe",

    # Location of the ftjam freetype build system executable
    "FTJAM_EXECUTABLE:FILEPATH": "C:/Tools/ftjam-2.5.2/jam.exe",

    #Location where source tar-balls are (to be) downloaded.
    "download_location:PATH":"c:/bbd/superbuild-downloads",
}

defenv = {
    'JSDUCK_HOME': 'C:/Tools/jsduck-4.4.1',
}

#------------------------------------------------------------------------------
# VS9 (2008) 64-bit properties and environment.
#------------------------------------------------------------------------------
vs9x64props = {
    'compiler': 'msvc-2008-x64',
    'vcvarsall': 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument': 'amd64',
}

vs9x64env = {
    'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x64/bin;${PATH}'
}

vs9x64config = {
    'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Tools/qt-4.8.4/vs2008-x64/bin/qmake.exe'
}

#------------------------------------------------------------------------------
# VS9 (2008) 32-bit properties and environment.
#------------------------------------------------------------------------------
vs9x32props = {
    'compiler': 'msvc-2008-x86',
    'vcvarsall': 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument': 'x86',
}

vs9x32env= {
    'PATH':'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x32/bin;${PATH}'
}

vs9x32config = {
}

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, vtksuperbuild, buildsets,
    defprops=projects.merge_config(defprops, vs9x64props),
    defconfig=projects.merge_config(defconfig, vs9x64config),
    dirlen=8,
    env=projects.merge_config(defenv, vs9x64env)
)

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild','32bit',),
    },
]

BUILDERS.extend(projects.make_builders(slave.SLAVE, vtksuperbuild, buildsets,
    defprops=projects.merge_config(defprops, vs9x32props),
    defconfig=projects.merge_config(defconfig, vs9x32config),
    dirlen=8,
    env=projects.merge_config(defenv, vs9x32env)
))

import projects
from projects import vtksuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        "7Z_EXE:FILEPATH": "C:/Program Files/7-Zip/7z.exe",

        # Location of the ftjam freetype build system executable
        "FTJAM_EXECUTABLE:FILEPATH": "C:/Tools/ftjam-2.5.2/jam.exe",

        #Location where source tar-balls are (to be) downloaded.
        "download_location:PATH":"c:/bbd/superbuild-downloads",

        #common options for java on this machine
        "JOGL_GLUE:FILEPATH": "C:/Users/utkarsh/.m2/repository/org/jogamp/gluegen/gluegen-rt/2.0.2/gluegen-rt-2.0.2.jar",
        "JOGL_LIB:FILEPATH": "C:/Users/utkarsh/.m2/repository/org/jogamp/jogl/jogl-all/2.0.2/jogl-all-2.0.2.jar",
    },

    'slaveenv': {
        'JSDUCK_HOME': 'C:/Tools/jsduck-4.4.1',
    },
}


#------------------------------------------------------------------------------
vs9props = {
    'vcvarsall': 'C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/vcvarsall.bat',
}

#------------------------------------------------------------------------------
x64props = {
    'compiler': 'msvc-2008-x64',
    'vcvarsargument': 'amd64',

    'configure_options:builderconfig': {
        "JAVA_AWT_INCLUDE_PATH:PATH": "C:/Dashboards/Support/jdk7-x64/include",
        "JAVA_INCLUDE_PATH:PATH": "C:/Dashboards/Support/jdk7-x64/include",
        "JAVA_INCLUDE_PATH2:PATH": "C:/Dashboards/Support/jdk7-x64/include/win32",
        "JAVA_JVM_LIBRARY:PATH": "C:/Dashboards/Support/jdk7-x64/lib/jvm.lib",
        "JAVA_AWT_LIBRARY:PATH": "C:/Dashboards/Support/jdk7-x64/lib/jawt.lib",
        "Java_JAR_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x64/bin/jar.exe",
        "Java_JAVAC_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x64/bin/javac.exe",
        "Java_JAVADOC_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x64/bin/javadoc.exe",
        "Java_JAVAH_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x64/bin/javah.exe",
        "Java_JAVA_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x64/bin/java.exe",
    },

    'slaveenv': {
        'JDK_HOME': 'C:/Dashboards/Support/jdk7-x64',
        'PATH': 'C:/Tools/jom;C:/Dashboards/Support/jdk7-x64/jre/bin;${PATH}'
    },
}

x32props = {
    'compiler': 'msvc-2008-x32',
    'vcvarsargument': 'x86',

    'configure_options:builderconfig': {
        "JAVA_AWT_INCLUDE_PATH:PATH": "C:/Dashboards/Support/jdk7-x32/include",
        "JAVA_INCLUDE_PATH:PATH": "C:/Dashboards/Support/jdk7-x32/include",
        "JAVA_INCLUDE_PATH2:PATH": "C:/Dashboards/Support/jdk7-x32/include/win32",
        "JAVA_JVM_LIBRARY:PATH": "C:/Dashboards/Support/jdk7-x32/lib/jvm.lib",
        "JAVA_AWT_LIBRARY:PATH": "C:/Dashboards/Support/jdk7-x32/lib/jawt.lib",
        "Java_JAR_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x32/bin/jar.exe",
        "Java_JAVAC_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x32/bin/javac.exe",
        "Java_JAVADOC_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x32/bin/javadoc.exe",
        "Java_JAVAH_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x32/bin/javah.exe",
        "Java_JAVA_EXECUTABLE:FILEPATH": "C:/Dashboards/Support/jdk7-x32/bin/java.exe",
    },

    'slaveenv': {
        'JDK_HOME': 'C:/Dashboards/Support/jdk7-x32',
        'PATH': 'C:/Tools/jom;C:/Dashboards/Support/jdk7-x32/jre/bin;${PATH}'
    },
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

BUILDERS = projects.make_builders(slave, vtksuperbuild, buildsets,
    projects.merge_config(defprops, vs9props, x64props),
    dirlen=8)

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild','32bit',),
    },
]

BUILDERS += projects.make_builders(slave, vtksuperbuild, buildsets,
    projects.merge_config(defprops, vs9props, x32props),
    dirlen=8)

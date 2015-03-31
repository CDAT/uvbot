import projects
from projects import vtksuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

BUILDERS = []

defprops = {
    'configure_options:builderconfig': {
        'CMAKE_OSX_ARCHITECTURES:STRING': 'x86_64',

        'download_location:PATH': '/Users/kitware/Dashboards/MyTests/VTKSuperbuild-downloads',

        'JAVA_AWT_INCLUDE_PATH:PATH': '/System/Library/Frameworks/JavaVM.framework/Headers',
        'JAVA_INCLUDE_PATH:PATH': '/System/Library/Frameworks/JavaVM.framework/Headers',
        'JAVA_INCLUDE_PATH2:PATH': '/System/Library/Frameworks/JavaVM.framework/Headers',

        'JAVA_JVM_LIBRARY:PATH': '-framework JavaVM',
        'JAVA_AWT_LIBRARY:PATH': '-framework JavaVM',

        'Java_JAR_EXECUTABLE:FILEPATH': '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/jar',
        'Java_JAVAC_EXECUTABLE:FILEPATH': '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/javac',
        'Java_JAVADOC_EXECUTABLE:FILEPATH': '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/javadoc',
        'Java_JAVAH_EXECUTABLE:FILEPATH': '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/javah',
        'Java_JAVA_EXECUTABLE:FILEPATH': '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/java',
    },
}

buildsets = [
    {
        'os': 'osx',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'osx10.5',
            'superbuild',
        ),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, vtksuperbuild, buildsets, defprops)


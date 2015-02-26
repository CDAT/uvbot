from buildbot.buildslave import BuildSlave

# The master machine stores secrets on disk to keep them out of the history.
# This module provides this information.
from machines import secrets

__all__ = [
    'SLAVE',
]

# The first arguments are the name of the slave and the password the slave will
# use to communicate with the master server.
SLAVE = BuildSlave('_example', secrets.SECRETS['_example']['password'],
    # The maximum number of concurrent builds the machine may run.
    max_builds=1,
    properties={
        # REQUIRED: The prefix path for CMake (.../bin/cmake should exist under here).
        'cmakeroot': '/opt/apps/cmake-3.0.1',
        # Where projects may store information on the machine (data, results, etc.).
        'sharedresourcesroot': '/home/kitware/Dashboards/MyTests',

        # The operating system; one of: ('linux', 'windows', 'osx')
        'os': 'linux',
        # Description of the install. Keep it lowercase and in a
        # '$os-$version-$arch' format. For Linux, the name of the distribution
        # and its version should be used.
        'distribution': 'ubuntu-12.04-x86_64',
        # The compiler and its version.
        'compiler': 'gcc-4.6.3',

        # The CMake generator to use.
        'generator': 'Unix Makefiles',
        # Flags to pass to the build tool (for parallelism). Also recommended
        # is `-l#` (load average) for machines with concurrent builds to not
        # swamp the machine.
        'buildflags': '-j9',

        # CMake options *all* projects with this slave should receive.
        'configure_options:buildslave': {
            'CMAKE_CXX_FLAGS:STRING': '-Wall -Wextra -Wshadow -Woverloaded-virtual -Wno-deprecated',
            'CMAKE_C_FLAGS:STRING': '-Wall -Wextra -Wshadow',
        },

        # Environment variables which should be used on the slave for *all*
        # projects. Existing environment variables may be referenced as
        # `${ENVVAR}` (the braces are important).
        'env': {
            'PATH': '/path/for/ninja:${PATH}',
        },
    }
)

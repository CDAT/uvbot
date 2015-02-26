import projects
from projects import project1

__all__ = [
    'BUILDERS',
]

defprops = {
    # Labels to *include* in the testing for all builds of this project.
    'test_include_labels:builderconfig': [
        'LABEL1',
        'LABEL2',
    ],
    # Tests to exclude for this project. Please ensure that excluded tests are
    # commented. These values are regular expressions, so be careful with the
    # relevant special characters.
    'test_excludes:builderconfig': [
        'test1', # gremlins
        'test2', # bogus drivers
        'some.*test.*regex', # runs out of memory
    ],
}
# Relevant environment variables for this project.
env = {
    'DISPLAY': ':0',
}

# Common CMake configuration values for this project. The project may provide
# default configuration to use, so use that if possible.
#defconfig = project1.CONFIG.copy().update({...})
defconfig = {
    'BUILD_EXAMPLES:BOOL': 'ON',
    'VTK_DEBUG_LEAKS:BOOL': 'ON',
    'PARAVIEW_BUILD_CATALYST_ADAPTORS:BOOL': 'ON',
    'PARAVIEW_DATA_STORE:PATH': '/home/kitware/Dashboards/MyTests/ExternalData',

    'PARAVIEW_BUILD_PLUGIN_MantaView:BOOL': 'ON',
    'MANTA_BUILD:PATH': '/opt/source/manta-build',

    'smooth_flash:FILEPATH': '/home/kitware/Dashboards/MyTests/ParaViewSuperLargeData/smooth.flash',

    'PARAVIEW_ENABLE_COSMOTOOLS:BOOL': 'ON',
    'GENERIC_IO_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Support/Cosmology/genericio',
    'GENERIC_IO_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/genericio-build/libGenericIO.a',
    'COSMOTOOLS_INCLUDE_DIR:PATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/include',
    'COSMOTOOLS_LIBRARIES:FILEPATH': '/home/kitware/Dashboards/Support/Cosmology/cosmologytools-build/libs/libcosmotools.a',
}

# A list of 'buildsets' for a project. Projects have 'options' and 'features'.
# All options are required and have a set of understood values. Usually, they
# contain supplemental CMake configuration as well. Typical options include
# 'os' for the host operating system, 'libtype' for shared or static, and
# 'buildtype' for choosing between release and debug builds. Features are
# extras which may be added to builds. Features not specified are turned off to
# keep a 1:1 relationship between the buildname and what is actually tested.

# Features all builds should include.
base_features = (
    'featurea',
)
buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'debug',
        'features': base_features,
    },
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'debug',
        'features': base_features + (
            'featureb',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': base_features,
    },
]

# The 'projects' module contains a `make_builders` function which takes the
# project and buildsets and generates the proper build name and CMake
# configuration for each.
BUILDERS = projects.make_builders(project1, buildsets,
    # The base properties to build upon.
    defprops=defprops,
    # The CMake variables to build upon.
    defconfig=defconfig,
    # The slave which should build these (should match the slave in this directory).
    slavenames=['blight'],
    # Other keyword arguments are passed to the BuilderConfig constructor.
    # Important ones may include 'category' for putting the builds into a
    # category for separating the builds out in the view and 'env' for
    # environment variables.
    category='awesome',
    env=env
)

# the 'projects' module contains a `merge_config` function which will join two
# dictionaries. For each item, it appends lists together, recursively merges
# dictionary values, and replaces other types. Mismatches between the
# dictionaries will trigger an error. This is useful for making more builders
# which share other options which are not necessary for other builds.
specialprops = projects.merge_config(defprops, {
    # Append an extra test to exclude
    'test_excludes:builderconfig': [
        'flyingpigs', # full moon on Tuesdays
    ]
})
# More environment variables.
specialenv = projects.merge_config(env, {
    'PATH': '/path/to/some/tool:${PATH}',
})

specialbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'special',
        )
    },
]

# Make sure to *append* these new buildsets.
BUILDERS += projects.make_builders(project1, specialbuildsets,
    defprops=specialprops,
    defconfig=defconfig,
    slavenames=['blight'],
    env=qt5env
)

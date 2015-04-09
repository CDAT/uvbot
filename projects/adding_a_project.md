Adding a Project
================

Projects are stored in `projects/` as a subdirectory.  Each project has four
main files.

## Gitlab Project Definition

The file `projects/X/poll.py` contains information about where to get the
project.  It should have the following contents:

```python
__all__ = [
    'REPO',
    'BRANCHES',
    'CDASH_ROOT',
    'CDASH_PROJECTNAME',
]

# The name of the origin repository on Gitlab
REPO = 'VTK/VTK'
# Any integration branches to be tested
BRANCHES = [
    'master',
]
# Where to post CDash results
CDASH_ROOT = 'https://open.cdash.org'
# The name of the project on CDash
CDASH_PROJECTNAME = 'VTK'
```

## Project Configuration Options
The file `projects/X/__init__.py` contains the configuration options
for the project.  This file should minimally contain the following:

```python
__all__ = [
    'NAME',
    'DEFAULTS',
    'OPTIONS',
    'OPTIONORDER',
    'FEATURES',
]

NAME = 'X'

DEFAULTS = {}

OPTIONS = {}

OPTIONORDER = ()

FEATURES = {}
```

`NAME` contains the name of the project.

`DEFAULTS` is a hash of project-wide properties. Properties are used by
buildbot to determine how to perform parts of the build. By default,
the buildslave properties will overwrite any builder properties. Instead,
we use "composite keys" to override this behavior for certain keys. These keys
have four levels: *buildslave*, *builderconfig*, *project*, and *feature*.
Properties suffixed with this subkey (with a colon) are merged together with
later levels overriding earlier levels. Lists and dictionaries are merged when
this happens. The keys which use this are: `generator`, `buildflags`,
`configure_options`, `test_include_labels`, `test_excludes`,
`upload_file_patterns`, and `supports_parallel_testing`. Below is an example
`DEFAULTS` hash.

```python
DEFAULTS = {
    'configure_options:project': {
        'BUILD_EXAMPLES:BOOL': 'ON',
        'BUILD_TESTING:BOOL': 'ON',
        'VTK_DEBUG_LEAKS:BOOL': 'ON',
        'VTK_LEGACY_REMOVE:BOOL': 'ON',
        'VTK_USER_LARGE_DATA:BOOL': 'ON',
    },
    'supports_parallel_testing:project' : True,

    'cdash_url': 'https://open.cdash.org',
    'cdash_project': 'VTK',
}
```

This hash defines two global properties, the `cdash_url` and `cdash_project`
and two project-level properties: `configure_options` and
`supports_parallel_testing`.  The cdash-related properties are defined global
since it does not make sense for anything else to override them.  The most
common property is `configure_options`, which is a key-value map of CMake
variables to pass to the configure step.  The `supports_parallel_testing`
property is used by the default test step to determine whether to use the
`PARALLEL_LEVEL` option of `ctest_test`.

`OPTIONS` is a dictionary of required build parameters.  This means parameters
such as `os` which will be valid for all builds.  The value of the dictionary
is a map of possible values of the option to additional properties they imply.
For example:

```python
OPTIONS = {
    'libtype': {
        'shared': {
             'configure_options:project': {
                 'BUILD_SHARED_LIBS:BOOL', 'ON',
             },
        },
        'static': {
             'configure_options:project': {
                 'BUILD_SHARED_LIBS:BOOL', 'OFF',
             },
        },
    },
}
```

The value for the `libtype` option of this project must always be either
`shared` or `static`.  If `shared` is selected then the property to tell
CMake to turn on shared libs is added to the properties of the build.

Several common option maps are defined in `projects/common/options.py` and
can be used by importing that file.  For example the above `OPTIONS` map
can be rewritten as:

```python
from projects.common import options
OPTIONS = {
    'libtype': options.libtypes,
}
```

These common options include `os`, `libtype`, `buildtype` and `category`.

`OPTIONORDER` is a list of the option names (`libtype` in the above example)
to determine in what order the options are appended into the build name.
Options not listed here will not appear in the build name.

`FEATURES` is a dictionary of optional build parameters that can be enabled or
disabled in a build.  Unlike options, features only have two states, on and off
and their value is a tuple of dictionaries, the first being the properties set
if the feature is off and the second the properties set if the feature is on.
Here is an example of setting feature-level configure options to enable Python
in VTK:

```python
FEATURES = {
    'python': ({
        'configure_options:feature': {
            'VTK_WRAP_PYTHON:BOOL': 'OFF',
        },
    },{
        'configure_options:feature': {
            'VTK_WRAP_PYTHON:BOOL': 'ON',
        },
    })
}
```

Often, features are simply a switch for a CMake variable ON or OFF.  A shortcut
for this type of feature is provided in the `projects` module.  Using this, the
above code becomes:

```python
FEATURES = {
    'python': projects.make_feature_cmake_options({
        'VTK_WRAP_PYTHON:BOOL': ('OFF', 'ON'),
    }),
}
```

Multiple CMake options can be passed in this dictionary with a tuple for their
value and the correct feature description dictionary will be created.  This
function also takes keyword arguments `extra_with` and `extra_without` for
properties that should only be set in one state of the feature.

Similar to the common options above, there are common features that projects
may share in `projects/common/features.py`.  These are things like using the
clang or icc compilers or overriding the `supports_parallel_testing` value for
the project.  Features that are enabled for a build are appended to the build
name unless their names start with `_`.

## Project Build Schedulers

The next part of a project is the schedulers.  These are typically generated
by `projects/X/schedule.py` in a `make_schedulers` function which returns a
list of schedulers when passed a list of buildnames.  Here is a simple example
that forces a build of a builder when a button is pressed in the web interface.

```python
__all__ = [ 'make_schedulers', ]

def make_schedulers(buildnames):
    return [
        ForceScheduler(
            name='My Project Scheduler',
            builderNames=buildnames,
            branch=FixedParameter(name='branch', default='master'),
            username=UserNameParameter(label='your name:<br>', size=80),
            project=FixedParameter(name='project', default='X'),
            revision=FixedParameter(name='project', default=''),
            repository=FixedParameter(name='repository', default='path/to/my/repository.git'),
       ),
    ]
```
Please note that scheduler names must be unique between all projects and
builders.

For more types of schedulers, including those that fire off builds when a
branch is updated, see [the buildbot documentation](
http://docs.buildbot.net/current/manual/cfg-schedulers.html)
or copy and modify an existing schedulers file.

## The Factory: How to Build Your Project

The `projects/X/factory.py` file creates a buildbot factory object.  The
factory contains a list of steps that will be run on each slave to build
and test the project.  Many common types of steps used by Kitware projects
can be found in `kwextensions/steps.py`.  The factory file must define the
following:

```python
__all__ = [
    "get_factory",
    "get_source_steps",
]

def get_source_steps(sourcedir="source"):
    ...

def get_factory(buildset):
    ...
```

The `get_source_steps` function should return the steps needed to checkout the
source of the project properly.  The sourcedir parameter is where, relative to
the builder folder to check out the source.  The `get_factory` function should
return a `buildbot.process.factory.BuildFactory` instance that has all the
steps needed for a full build and test added to it.  Usually `get_factory` will
use `get_source_steps` internally.

## Enabling Your Project

After you have the above files written there are three more things to do before
your project will be built.  First, add the project name to the `PROJECTS` list
in `projects/__init__.py`.  Second, add the project and its schedule module as a
key/value pair in the `SCHEDULES` dictionary in `projects/schedulers.py`.  Third
add a machine with builders for your project.

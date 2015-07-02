from importlib import import_module
import copy
import hashlib

from buildbot.config import BuilderConfig
from datetime import datetime


__all__ = [
    'build_config',
    'make_feature_cmake_options',
    'make_builders',
    'merge_config',
    'PROJECTS',
]


PROJECTS = [
     'geojs',
     'uvcdat'
#    # VTK
#    'VTK',
#    'VTKSuperbuild',
#
#    # ParaView
#    'ParaView',
#    'ParaViewSuperbuild',
#    'Catalyst',
#
#    # CMB
#    'CMB',
#    'CMBSuperbuild',
]


def build_config(project, props, features=(), **kwargs):
    avail_options = set(project.OPTIONS.keys())
    avail_features = set(project.FEATURES.keys())

    buildset = kwargs.copy()

    options = set(buildset.keys())
    missing_options = []

    # update buildset and options with missing options that have 'default'
    # with specified default value.
    for mo in avail_options.difference(options):
        try:
            buildset[mo] = project.OPTIONS.get(mo)['default']
            options.add(mo)
        except KeyError:
            missing_options.append(mo)

    if missing_options:
        raise RuntimeError('unknown missing options: %s' % ', '.join(missing_options))

    unknown_options = options.difference(avail_options)
    if unknown_options:
        print('ignoring unknown options: %s' % ', '.join(unknown_options))

    featureset = set(features)
    unknown_features = featureset.difference(avail_features)
    if unknown_features:
        raise RuntimeError('unknown features: %s' % ', '.join(unknown_features))

    allprops = props.copy()

    for optname, optvalues in project.OPTIONS.items():
        if buildset[optname] not in optvalues:
            raise RuntimeError('unknown value for option %s: %s' % (optname, buildset[optname]))

        allprops = merge_config(allprops, optvalues[buildset[optname]])

    nameparts = []
    for option in project.OPTIONORDER:
        nameparts.append(buildset[option])
    name = '-'.join(nameparts)

    for feature in sorted(avail_features):
        use_feature = 0
        if feature in featureset:
            if not feature.startswith('_'):
                name += '+%s' % feature
            use_feature = 1
        props = project.FEATURES[feature][use_feature]
        allprops = merge_config(allprops, props)

    return (name, allprops, buildset)


def make_feature_cmake_options(options, extra_without={}, extra_with={}):
    with_feature = {}
    without_feature = {}

    for k, (off, on) in options.items():
        with_feature[k] = on
        without_feature[k] = off

    return (
        merge_config({'configure_options:feature': without_feature}, extra_without),
        merge_config({'configure_options:feature': with_feature}, extra_with),
    )


def _merge_options(props, key, default):
    subkeys = [
        'buildslave',
        'builderconfig',
        'project',
        'feature',
        'priority',
    ]
    merged = merge_config(props, {key: default})
    for subkey in subkeys:
        fullkey = '%s:%s' % (key, subkey)
        if fullkey not in props:
            continue
        merged = merge_config(merged, {key: props[fullkey]})
    return merged


def make_builders(slave, project, buildsets, props, dirlen=0, **kwargs):
    baseprops = merge_config(project.DEFAULTS.copy(), slave.SLAVEPROPS, props)

    setprops = {}
    for buildset in buildsets:
        name, buildsetprops, buildset = build_config(project, baseprops, **buildset)
        setprops[name] = (buildsetprops, buildset)

    # import factory module for the provided project.
    factory = import_module("%s.factory" % project.__name__)

    composite_keys = (
        ('generator', None),
        ('buildflags', ''),
        ('configure_options', {}),
        ('test_include_labels', []),
        ('test_excludes', []),
        ('upload_file_patterns', []),
        ('supports_parallel_testing', False),
    )

    default_category = project.OPTIONS.get('category', {}).get('default')

    builders = []
    for name, (buildprops, buildset) in setprops.items():
        buildprops['buildset'] = buildset
        for key, default in composite_keys:
            buildprops = _merge_options(buildprops, key, default)

        # if buildset has a option named category, use that to generate a
        # category for the builder. If not, we simply use the project's name as
        # the category.
        builder_category = project.NAME
        if 'category' in buildset:
            category = buildset['category']
            buildprops['dashboard_status'] = category
            builder_category = "-".join([project.NAME, category])

            if category != default_category:
                if 'ctest_track_suffix' in buildprops:
                    buildprops['ctest_track_suffix'] += '-%s' % category
                else:
                    buildprops['ctest_track_suffix'] = '-%s' % category

        buildname = '%s-%s-%s' % (project.NAME, slave.SLAVE.slavename, name)

        if dirlen:
            kwargs['slavebuilddir'] = hashlib.md5(buildname).hexdigest()[:dirlen]

#        if buildprops['generator'] is None:
#            raise RuntimeError, 'no generator for build: %s' % buildname

        builders.append(BuilderConfig(
            name=buildname,
            factory=factory.get_factory(buildset),
            properties=buildprops,
            slavenames=[slave.SLAVE.slavename],
            category=builder_category,
            env=buildprops.get('slaveenv', {}),
            nextBuild=_pick_next_build,
            **kwargs
        ))

    return builders


def merge_config(base, *args):
    output = copy.deepcopy(base)

    for d in args:
        for k, v in d.items():
            if k in output:
                # Merge dictionaries.
                if type(v) == dict:
                    if type(output[k]) == dict:
                        output[k] = merge_config(output[k], v)
                    else:
                        raise RuntimeError('incompatible entries with key \'%s\'' % k)

                # Concatenate lists.
                elif type(v) == list:
                    if type(output[k]) == list:
                        output[k] += v
                    else:
                        raise RuntimeError('incompatible entries with key \'%s\'' % k)

                # Overwrite otherwise.
                else:
                    output[k] = v
            else:
                output[k] = v

    return output


def get_codebase(project=None, poll=None, secrets={}):
    """Returns the defaults to use for the projects code base"""
    if poll is None:
        poll = import_module("%s.poll" % project.__name__)
    return {
        get_codebase_name(poll.REPO) : {
            "repository" : poll.REPO,
            "branch" : "master",
            "revision" : None,
        }
    }

def get_codebase_name(projectname):
    # evidently codebase names must be alpha-numeric, so we just strip non-alpha
    # numeric characters from the project name.
    return "".join([x for x in projectname if x.isalnum()])

def codebaseGenerator(chdict):
    """Returns a codebase identifier for a given change."""
    # evidently codebase names must be alpha-numeric, so we just strip non-alpha
    # numeric characters from the project name.
    return get_codebase_name(str(chdict["project"]))

def get_change_filter_fn_for_buildbot_commands(accepted_values=[]):
    """Returns a function that can be used as a
    buildbot.changes.filter.ChangeFilter's filter_fn to test if the
    change has a `buildbot_commands` property with one of the
    `accepted_values` in it."""
    assert type(accepted_values) == list
    accepted_values = set(accepted_values)
    def filter_fn(change):
        cur_value = change.properties.getProperty('buildbot_commands', [])
        assert type(cur_value) == list
        # if any command in accepted_values is in cur_value, we're golden!
        return True if accepted_values.intersection(cur_value) else False
    return filter_fn

def _pick_next_build(bldr, requests):
    """Function to determine which build to process next for a builder.
    We'll prioritize 'merge-request' except between 8 pm and 6 am, when
    we prioritize 'integration-branch' changes."""
    now = datetime.now()
    if now.hour >= 20 or now.hour < 6:
        priority_category = 'integration-branch'
    else:
        priority_category = 'merge-request'
    for r in requests:
        for c in r.source.changes:
            if c.category == priority_category:
                return r
    return requests[0]
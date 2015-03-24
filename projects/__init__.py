from importlib import import_module
import copy
import hashlib

from buildbot.config import BuilderConfig


__all__ = [
    'build_config',
    'make_builders',
    'merge_config',
    'PROJECTS',
]


PROJECTS = [
    # VTK
    'VTK',

    # ParaView
    'ParaView',
    'ParaViewSuperbuild',
    'Catalyst',
]


def build_config(project, defconfig={}, features=(), **kwargs):
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

    config = defconfig.copy()

    for optname, optvalues in project.OPTIONS.items():
        if buildset[optname] not in optvalues:
            raise RuntimeError('unknown value for option %s: %s' % (optname, buildset[optname]))

        config.update(optvalues[buildset[optname]])

    nameparts = []
    for option in project.OPTIONORDER:
        nameparts.append(buildset[option])
    name = '-'.join(nameparts)

    for feature in sorted(avail_features):
        use_feature = 0
        if feature in featureset:
            name += '+%s' % feature
            use_feature = 1
        for k, v in project.FEATURES[feature].items():
            config[k] = v[use_feature]

    return (name, config, buildset)


def _merge_options(props, key, default):
    subkeys = [
        'buildslave',
        'builderconfig',
        'project',
        'feature',
    ]
    merged = merge_config(props, {key: default})
    for subkey in subkeys:
        fullkey = '%s:%s' % (key, subkey)
        if fullkey not in props:
            continue
        merged = merge_config(merged, {key: props[fullkey]})
    return merged


def make_builders(slave, project, buildsets, defprops={}, defconfig={}, myfactory=None, dirlen=0, **kwargs):
    configs = {}
    for buildset in buildsets:
        name, conf, buildset = build_config(project, defconfig=defconfig, **buildset)
        configs[name] = (conf, buildset)

    if not myfactory is None:
        raise RuntimeError("'myfactory' is no longer supported!")

    # import factory module for the provided project.
    factory = import_module("%s.factory" % project.__name__)

    composite_keys = (
        ('configure_options', {}),
        ('test_include_labels', []),
        ('test_excludes', []),
        ('upload_file_patterns', []),
    )

    builders = []
    for name, (config, buildset) in configs.items():
        props = defprops.copy()
        props['configure_options:builderconfig'] = config

        for key, default in composite_keys:
            props = _merge_options(props, key, default)

        if dirlen:
            kwargs['slavebuilddir'] = hashlib.md5(name).hexdigest()[:dirlen]

        # if buildset has a option named category, use that to generate a
        # category for the builder. If not, we simply use the project's name as
        # the category.
        try:
            category = buildset['category']
            builder_category = "-".join([project.NAME, category])

            # add category to track name if its not the default.
            default_category = project.OPTIONS.get('category').get('default')
            if category != default_category:
                props['ctest_track_suffix'] = "%s-%s" % (props.get('ctest_track_suffix',""), category)
        except KeyError:
            builder_category = project.NAME

        builders.append(BuilderConfig(
            name='%s-%s-%s' % (project.NAME, slave.slavename, name),
            factory=factory.get_factory(buildset),
            properties=props,
            slavenames=[slave.slavename],
            category=builder_category,
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
            "repository" : "https://%s/%s.git" % (secrets['gitlab_host'], poll.REPO.lower()),
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

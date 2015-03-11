import copy
import hashlib

from buildbot.config import BuilderConfig

from kwextensions import factory


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


def build_config(project, defconfig={}, features=(), *args, **kwargs):
    avail_options = set(project.OPTIONS.keys())
    avail_features = set(project.FEATURES.keys())

    options = set(kwargs.keys())
    missing_options = avail_options.difference(options)
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
        if kwargs[optname] not in optvalues:
            raise RuntimeError('unknown value for option %s: %s' % (optname, kwargs[optname]))

        config.update(optvalues[kwargs[optname]])

    nameparts = []
    for option in project.OPTIONORDER:
        nameparts.append(kwargs[option])
    name = '-'.join(nameparts)

    for feature in sorted(avail_features):
        use_feature = 0
        if feature in featureset:
            name += '+%s' % feature
            use_feature = 1
        for k, v in project.FEATURES[feature].items():
            config[k] = v[use_feature]

    return (name, config)


def make_builders(slave, project, buildsets, defprops={}, defconfig={}, myfactory=None, dirlen=0, **kwargs):
    configs = {}
    for buildset in buildsets:
        name, conf = build_config(project, defconfig=defconfig, **buildset)
        configs[name] = conf

    if myfactory is None:
        myfactory = factory.get_ctest_buildfactory()

    builders = []
    for name, config in configs.items():
        props = defprops.copy()
        props['configure_options:builderconfig'] = config

        if dirlen:
            kwargs['slavebuilddir'] = hashlib.md5(name).hexdigest()[:dirlen]

        builders.append(BuilderConfig(
            name='%s-%s' % (slave.slavename, name),
            factory=myfactory,
            properties=props,
            slavenames=[slave.slavename],
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
                        merge_config(output[k], v)
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

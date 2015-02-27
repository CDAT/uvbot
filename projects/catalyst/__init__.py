
__all__ = [
    'NAME',
    'OPTIONS',
    'OPTIONORDER',

    'FEATURES',
]

NAME = 'catalyst'

OPTIONS = {
    'os': {
        'linux': {},
        'osx': {},
    },
    'editionset' : {
        'Base' : {},
        'Base+Essentials' : {},
        'Base+Essentials+Extras' : {},
        'Base+Essentials+Extras+Rendering-Base' : {},
        'Base+Enable-Python' : {},
        'Base+Enable-Python+Essentials' : {},
        'Base+Enable-Python+Essentials+Extras' : {},
        'Base+Enable-Python+Essentials+Extras+Rendering-Base+Rendering-Base-Python' : {},
    }
}

OPTIONORDER = ('os', 'editionset')

FEATURES = {}

def make_builders(project, buildsets, defprops={}, defconfig={}, **kwargs):
    from kwextensions.factory import get_catalyst_buildfactory
    from .. import make_builders as mb
    mybuilders = list()
    # make builders one at a time to add the editionset property
    for buildset in buildsets:
        props = defprops.copy()
        # override to upload source tarball to cdash
        props['catalyst:upload_source_tarball'] = 0
        props['catalyst:catalyst_editions_required'] = buildset['editionset'].split('+')
        builders = mb(project,[buildset,],defprops=props,
                      defconfig=defconfig,
                      myfactory=get_catalyst_buildfactory(),
                      **kwargs)
        mybuilders += builders
    return mybuilders

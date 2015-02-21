from buildbot.buildslave import BuildSlave as _BuildSlave
import pickle

class BuildSlave(_BuildSlave):
    """Extends buildbot.buildslave.BuildSlave to add parameters
    needed in our slaves configurations."""
    def __init__(self, name, password,
                 cmake_root,
                 shared_resources_root,
                 env={},
                 **kwargs):
        """
        @param cmake_root:
            Root directory for cmake to use. e.g. for
            '/opt/apps/cmake-3.0.1/bin/cmake', this will be set to '/opt/apps/cmake-3.0.1'
        @param shared_resources_root:
            Root directory under which various builds can share resources
            such as data directories or ExternalData_OBJECT_STORES.
        @param env:
            A dict of key value pairs to pass as the environment to any build step.
        @type env: dictionary
        """
        _BuildSlave.__init__(self, name, password, **kwargs)
        self.properties.setProperty('cmakeroot', cmake_root, 'BuildSlave')
        self.properties.setProperty('sharedresourcesroot', shared_resources_root, 'BuildSlave')
        self.properties.setProperty('slaveenv', pickle.dumps(env), 'BuildSlave')

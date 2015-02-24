from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from kwextensions import factory
from buildbot.process.properties import Property, Interpolate

slave = BuildSlave('neodymius', 'XXXXXXXX',
        max_builds=1,
        properties = {}
        )


def get_buildslave():
    """Returns the BuildSlave instance for this machine"""
    return slave

def get_builders(project="ParaView"):
    """Returns a list of build configurations for this slave for a specific project."""
    return []

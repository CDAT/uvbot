r'''
    Machine: crunchy.llnl.gov
    Owner: doutriaux1@llnl.gov
'''

from . import slave
from . import uvcdat

BUILDERS = {
    'uvcdat': uvcdat.BUILDERS
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

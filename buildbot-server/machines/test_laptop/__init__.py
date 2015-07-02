r'''
    Machine: garant.kitware.com
    Owner: jonathan.beezley@kitware.com
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

r'''
    Machine: garant.kitware.com
    Owner: jonathan.beezley@kitware.com
'''

from . import slave
from . import geojs

BUILDERS = {
    'geojs': geojs.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

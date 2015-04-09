r'''
    Machine: curius.kitwarein.com
    Owner: sankhesh.jhaveri@kitware.com
'''

from . import slave
from . import geojs

BUILDERS = {
    'GeoJS' : geojs.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

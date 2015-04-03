r'''
    Machine: debian-x64.kitware.com
    Owner: ben.boeckel@kitware.com
'''

from . import slave
from . import paraviewsuperbuild

BUILDERS = {
    'ParaViewSuperbuild': paraviewsuperbuild.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

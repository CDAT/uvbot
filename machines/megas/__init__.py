r'''
    Machine: megas.kitwarein.com
    Owner: ben.boeckel@kitware.com
'''

from . import slave
from . import paraview
from . import catalyst

BUILDERS = {
    'ParaView': paraview.BUILDERS,
    'Catalyst': catalyst.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

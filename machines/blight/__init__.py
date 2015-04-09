r'''
    Machine: blight.kitware.com
    Owner: utkarsh.ayachit@kitware.com
'''

from . import slave
from . import paraview
from . import paraviewsuperbuild

BUILDERS = {
    'ParaView': paraview.BUILDERS,
    'ParaViewSuperbuild': paraviewsuperbuild.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

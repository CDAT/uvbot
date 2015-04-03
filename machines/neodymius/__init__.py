r'''
    Machine: neodymius.kitware.com
    Owner: sankhesh.jhaveri@kitware.com
'''

from . import slave
from . import paraview
from . import vtk

BUILDERS = {
    'ParaView': paraview.BUILDERS,
    'VTK': vtk.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

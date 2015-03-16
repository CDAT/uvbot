r'''
    Machine: amber8.kitwarein.com
    Owner: vtk-developers@vtk.org
'''

from . import slave
from . import vtk
from . import paraview

BUILDERS = {
    'VTK': vtk.BUILDERS,
    'ParaView' : paraview.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

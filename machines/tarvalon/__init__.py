r'''
    Machine: tarvalonwin64.kitware.com
    Owner: robert.maynard@kitware.com
'''

from . import slave
from . import paraview
from . import vtk

BUILDERS = {
    'VTK': vtk.BUILDERS,
    'ParaView': paraview.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

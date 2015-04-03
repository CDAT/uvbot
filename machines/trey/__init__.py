r'''
    Machine: trey.kitware.com
    Owner: ben.boeckel@kitware.com
'''

from . import slave
from . import paraview
from . import paraviewsuperbuild
from . import vtk

BUILDERS = {
    'ParaView': paraview.BUILDERS,
    'ParaViewSuperbuild': paraviewsuperbuild.BUILDERS,
    'VTK': vtk.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

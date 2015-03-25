r'''
    Machine: amber8.kitwarein.com
    Owner: kitware-sysadmin@kitware.com
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

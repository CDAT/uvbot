r'''
    Machine: bigmac.kitwarein.com
    Owner: marcus.hanwell@kitware.com
'''

from . import slave
from . import paraviewsuperbuild
from . import paraview
from . import vtk

BUILDERS = {
#    'ParaViewSuperbuild': paraviewsuperbuild.BUILDERS,
    'ParaView' : paraview.BUILDERS,
    'VTK': vtk.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

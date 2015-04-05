r'''
    Machine: kamino.kitware.com
    Owner: dave.demarle@kitware.com
'''

from . import slave
from . import vtk
from . import vtksuperbuild

BUILDERS = {
    'VTK': vtk.BUILDERS,
    'VTKSuperbuild': vtksuperbuild.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

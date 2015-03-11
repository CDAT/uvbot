r'''
    Machine: tarvalon.kitwarein.com
    Owner: robert.maynard@kitware.com
'''

from . import slave
from . import vtk

BUILDERS = {
    'VTK': vtk.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

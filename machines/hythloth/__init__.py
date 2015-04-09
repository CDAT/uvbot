r'''
    Machine: hythloth.kitware.com
    Owner: brad.king@kitware.com
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

r'''
    Machine: renar.kitwarein.com
    Owner: robert.maynard@kitware.com
'''

from . import slave
from . import paraview

BUILDERS = {
    'ParaView': paraview.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

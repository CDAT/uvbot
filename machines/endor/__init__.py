r'''
    Machine: endor.kitware.com
    Owner: andy.bauer@kitware.com
'''

from . import slave
from . import cmb
from . import cmbsuperbuild

BUILDERS = {
    #'CMB': cmb.BUILDERS,
    'CMBSuperbuild': cmbsuperbuild.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

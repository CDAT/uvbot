r'''
    Machine: talosiv.kitwarein.com
    Owner: bob.obara@kitware.com
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

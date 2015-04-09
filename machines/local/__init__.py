r'''
    Machine: local
    Owner: you!
'''

from . import slave

class DummyProject(object):
    def __init__(self):
        self.BUILDERS = []

def try_import_project(project, scope):
    try:
        mod = __import__('machines.local.%s' % project, fromlist=['*'], level=1)
    except ImportError:
        mod = DummyProject()
    scope[project] = mod

try_import_project('geojs', globals())
#try_import_project('vtk', globals())
#try_import_project('vtksuperbuild', globals())
#
#try_import_project('catalyst', globals())
#try_import_project('paraview', globals())
#try_import_project('paraviewsuperbuild', globals())
#
#try_import_project('cmb', globals())
#try_import_project('cmbsuperbuild', globals())

BUILDERS = {
    'GeoJS': geojs.BUILDERS,
#    'VTK': vtk.BUILDERS,
#    'VTKSuperbuild': vtksuperbuild.BUILDERS,
#
#    'Catalyst': catalyst.BUILDERS,
#    'ParaView': paraview.BUILDERS,
#    'ParaViewSuperbuild': paraviewsuperbuild.BUILDERS,
#
#    'CMB': cmb.BUILDERS,
#    'CMBSuperbuild': cmbsuperbuild.BUILDERS,
}

def get_buildslave():
    return slave.SLAVE

def get_builders(project):
    return BUILDERS.get(project, [])

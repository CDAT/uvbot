# VTK
import vtk.schedule
import vtksuperbuild.schedule

# ParaView
import paraview.schedule
import paraviewsuperbuild.schedule
import catalyst.schedule

# CMB
import cmb.schedule
import cmbsuperbuild.schedule

# GeoJS
import geojs.schedule

__all__ = [
    'make_schedulers',
]


SCHEDULES = {
     # GeoJS
     'GeoJS' : geojs.schedule,

#    # VTK
#    'VTK' : vtk.schedule,
#    'VTKSuperbuild' : vtksuperbuild.schedule,
#
#    # ParaView
#    'ParaView': paraview.schedule,
#    'ParaViewSuperbuild': paraviewsuperbuild.schedule,
#    'Catalyst' : catalyst.schedule,
#
#    # CMB
#    'CMB': cmb.schedule,
#    'CMBSuperbuild': cmbsuperbuild.schedule,
}


def make_schedulers(project_builders, secrets):
    schedulers = []

    for project, builders in project_builders.items():
        if project not in SCHEDULES:
            raise RuntimeError('no schedule for %s' % project)

        buildnames = list(set([b.name for b in builders]))
        schedulers += SCHEDULES[project].make_schedulers(buildnames, secrets)

    return schedulers

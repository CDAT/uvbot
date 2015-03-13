# VTK
import vtk.schedule

# ParaView
import paraview.schedule
import paraviewsuperbuild.schedule
import catalyst.schedule


__all__ = [
    'make_schedulers',
]


SCHEDULES = {
    # VTK
    'VTK' : vtk.schedule,

    # ParaView
    'ParaView': paraview.schedule,
    'ParaViewSuperbuild': paraviewsuperbuild.schedule,
    'Catalyst' : catalyst.schedule,
}


def make_schedulers(project_builders):
    schedulers = []

    for project, builders in project_builders.items():
        if project not in SCHEDULES:
            raise RuntimeError('no schedule for %s' % project)

        buildnames = list(set([b.name for b in builders]))
        schedulers += SCHEDULES[project].make_schedulers(buildnames)

    return schedulers

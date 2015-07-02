# GeoJS
from geojs import schedule as geojs_schedule
from uvcdat import schedule as uvcdat_schedule

__all__ = [
    'make_schedulers',
]


SCHEDULES = {
     # GeoJS
     'geojs': geojs_schedule,
     'uvcdat': uvcdat_schedule,
}


def make_schedulers(project_builders, secrets):
    schedulers = []

    for project, builders in project_builders.items():
        if project not in SCHEDULES:
            raise RuntimeError('no schedule for %s' % project)

        buildnames = list(set([b.name for b in builders]))
        schedulers += SCHEDULES[project].make_schedulers(buildnames, secrets)

    return schedulers

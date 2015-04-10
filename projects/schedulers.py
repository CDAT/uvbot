# GeoJS
from geojs import schedule

__all__ = [
    'make_schedulers',
]


SCHEDULES = {
     # GeoJS
     'geojs': schedule,
}


def make_schedulers(project_builders, secrets):
    schedulers = []

    for project, builders in project_builders.items():
        if project not in SCHEDULES:
            raise RuntimeError('no schedule for %s' % project)

        buildnames = list(set([b.name for b in builders]))
        schedulers += SCHEDULES[project].make_schedulers(buildnames, secrets)

    return schedulers

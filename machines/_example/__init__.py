r'''
    Machine: $HOSTNAME.kitware.com
    Owner: $EMAIL_OF_WHO_HAS_ROOT
'''

# Store the slave description in a slave module.
from . import slave
# For each project built by this machine, import its module.
from . import project1

# Create a dictionary of projects to builders.
BUILDERS = {
    'Project1': project1.BUILDERS,
}

# Return the slave.
def get_buildslave():
    return slave.SLAVE

# Get the builders for a project.
def get_builders(project):
    return BUILDERS.get(project, [])

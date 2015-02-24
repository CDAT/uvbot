#!/usr/bin/bash

# This script will launch the buildbot slave on neodymius.

# since we're using mesa, no need to do offscreen screenshots.
export DISPLAY=:0

# Load intel compiler environment.
source /opt/intel/bin/compilervars.sh intel64

# Load modules needed for ParaView.
source /usr/share/Modules/init/bash
module load mpi/impi-x86_64

source /home/kitware/Dashboards/buildbot-sandbox/bin/activate
buildslave start /home/kitware/Dashboards/buildbot-slave

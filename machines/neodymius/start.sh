#!/bin/sh

# Load intel compiler environment.
source /opt/intel/bin/compilervars.sh intel64

# Load modules needed for ParaView.
source /usr/share/Modules/init/bash
module load mpi/impi-x86_64

source "$HOME/Dashboards/buildbot-sandbox/bin/activate"
buildslave start "$HOME/Dashboards/buildbot-slave"

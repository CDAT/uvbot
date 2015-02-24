#!/usr/bin/bash

# This script will launch the buildbot slave on neodymius.

# since we're using mesa, no need to do offscreen screenshots.
export DISPLAY=:0

source /home/kitware/Dashboards/buildbot-sandbox/bin/activate
buildslave start /home/kitware/Dashboards/buildbot-slave

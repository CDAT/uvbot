#!/bin/bash

# script to use to launch the buildbot slave on blight.
# This will setup the core environment for the slave.

# disable screensavers
gsettings set org.gnome.settings-daemon.plugins.power active false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false

xset -dpms
xset s off

source /opt/Modules/3.2.9/init/bash

# load needed modules.
module load cmake-3.0.1 mpich2-1.4.1p1 doxygen-1.8.8

# Add location of selenium chromedriver application to the path
export PATH=$PATH:/home/kitware/Dashboards/Support/chromedriver

# start the slave
/usr/local/bin/buildslave start /home/kitware/Dashboards/buildbot-slave

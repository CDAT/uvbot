#!/bin/sh

export WAR_PYTHON_VERSION=2.7 # osx is silly
exec wm-add-root buildbot -- buildslave start "$HOME/dashboards/buildbot"

set dashboardroot=%USERPROFILE%/dashboards/buildbot
set buildbotroot=%USERPROFILE%/misc/root/buildbot

set PYTHONPATH=%buildbotroot%/Lib/site-packages;%PYTHONPATH%

%buildbotroot%/Scripts/buildslave start %dashboardroot%

call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x64

set dashboardroot=%USERPROFILE%/dashboards/buildbot
set buildbotroot=%USERPROFILE%/misc/root/buildbot

set PYTHONPATH=%buildbotroot%/Lib/site-packages;%PYTHONPATH%

%buildbotroot%/Scripts/buildslave start %dashboardroot%

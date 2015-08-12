UV-CDAT buildbot setup
======================

This repository contains all the code necessary to create a new CI
service that works with UV-CDAT's github repository.  The setup
requires three components possibly on three seperate hosts:

1. A master server exposed to the internet that proxies github notifications
   and farm out to slaves
2. One or more build slaves that build and test the software and report
   statuses to both CDash and the Github status API (via the master)

Ports used in documentation bellow
----------------------------------

* 9981: master port
* 9982: slave port


Github repository setup
-----------------------

To register a new service with Github, you must have admin access to the
UV-CDAT repository.  Go to the project settings page, under "Webhooks & Services"
and choose the option "Add webhook".  Point the "Payload URL" to your github proxy
service (i.e. `http://yourserver.com:9981/master`),
choose "Content type" `application/json` and you are ready to receive the events.
For security, you should create a secret key to validate requests coming from Github.

You will also need to generate an access token to give the buildbot permission
to set statuses within the uvcdat repository.  You can generate one in your
user profile at [https://github.com/settings/tokens](https://github.com/settings/tokens).
Give the token a memeorable name and select only the `repo:status` checkbox.
Save the token string for later because you won't be able to access it after
you leave this page.


Master setup
------------

This repository contains a webservice implemented as a tangelo plugin.  The
service is implemented in [master/master.py](master/master.py).  You
will need to create config file in that directory named `projects.json` that
contains the following information:

```json
{
  "projects": {
    "UV-CDAT/uvcdat": {
      "bot-key": "*****",
      "api-key": "*****",
      "github-events": ["push"],
      "slaves" : ["http://myslaveserver:9982/slave"],
      "token": "*****",
      "logs_dir": "/Users/doutriaux1/uvbot-master/logs"
    }
  }
}
```

Where: 
* `bot-key` is a secret key that you will need to share with your slaves
* `api-key` is the key you setup on github in the section above
* `slaves` is a list of the urls of your slaves
* `token` is your git token setup in the github section above
* `logs_dir` a local directory where the master will stored build steps results from slaves

When that is done, install the requirements listed in [master/requirements.txt](master/requirements.txt)
and run
```
tangelo -r /path/to/slave --hostname myserver.com --port 9981
```
to start the service at `http://myserver.com:9981/master`.  See `tangelo -h` for more options.  When the service is running, you can test the connection by a get request
```
$ curl http://myserver.com:9981
How can I help you?
```

Buildbot slave setup
---------------------

The slave setup is very similar to the master one.
A webservice implemented as a tangelo plugin.  The
service is implemented in [slave/slave.py](slave/slave.py).  You
will need to create config file in that directory named `projects.json` that
contains the following information:

```json
{
  "projects": {
    "UV-CDAT/uvcdat": {
      "name": "SLAVE DESCRIPTION",
      "master": "http://myserver:9981/master",
      "bot-key": "****",
      "cmake_xtra": "-DCDAT_BUILD_MODE=LEAN",
      "build_parallel": 4,
      "ctest_xtra": "",
      "test_parallel": 4,
      "working_directory": "/Users/doutriaux1/uvcbot"
    }
  }
}
```

Where: 
* `name` is a short string describing the slave (to be used on github continuous
integration)
* `master` the url serving master
* `bot-key` is a secret key that you will need to obtain from the master admin
* `cmake_xtra` arguments you wish to pass to cmake
* `build_parallel` number of processors to use for build
* `ctest_xtra` extra args to pass to ctest
* `test_parallel` number of processors to use for ctest
* `working_directory` top directory for cloning and building

When that is done, install the requirements listed in [slave/requirements.txt](slave/requirements.txt)
and run
```
tangelo -r /path/to/slave --hostname myslaveserver.com --port 9982
```
to start the service at `http://myslaveserver.com:9981/slave`.  See `tangelo -h` for more options.  When the service is running, you can test the connection by a get request
```
$ curl http://myslaveserver.com:9982
How can I help you?
```

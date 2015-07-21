UV-CDAT buildbot setup
======================

This repository contains all the code necessary to create a new CI
service that works with UV-CDAT's github repository.  The setup
requires three components possibly on three seperate hosts:

1. An http server exposed to the internet that proxies github notifications
   to the buildbot master.
2. A buildbot master that maintains the build queue and manages the slaves.
3. One or more build slaves that build and test the software and report
   statuses to both CDash and the Github status API.


Github repository setup
-----------------------

To register a new service with Github, you must have admin access to the
UV-CDAT repository.  Go to the project settings page, under "Webhooks & Services"
and choose the option "Add webhook".  Point the "Payload URL" to your github proxy
service (i.e. `http://yourserver.com/proxy`),
choose "Content type" `application/json` and you are ready to receive the events.
For security, you should create a secret key to validate requests coming from Github.

You will also need to generate an access token to give the buildbot permission
to set statuses within the uvcdat repository.  You can generate one in your
user profile at [https://github.com/settings/tokens](https://github.com/settings/tokens).
Give the token a memeorable name and select only the `repo:status` checkbox.
Save the token string for later because you won't be able to access it after
you leave this page.


Github proxy setup
------------------

This repository contains a webservice implemented as a tangelo plugin.  The
service is implemented in [github-proxy/proxy.py](github-proxy/proxy.py).  You
will need to create config file in that directory named `projects.json` that
contains the following information:

```json
{
  "projects": {
    "UV-CDAT/uvcdat": {
      "api-key": "api-key-from-your-webhook-config",
      "buildbot": "http://your-buildbot-master:9989/",
      "user": "buildbot-user",
      "password": "buildbot-password",
      "events": ["push"]
    }
  }
}
```

When that is done, install the requirements listed in [github-proxy/requirements.txt](github-proxy/requirements.txt)
and run
```
tangelo -r /path/to/github-proxy --hostname myserver.com --port 8080
```
to start the service at `http://localhost:8080/proxy`.  See `tangelo -h` for more options.  When the service is running, you can test the connection by a get request
```
$ curl http://my-server.com:8080/proxy
How can I help you?
```

Buildbot master setup
---------------------

There are general instructions for setting up a new buildbot instance in
[buildbot-server/README.md](buildbot-server/README.md).  Some of the contents
of those instructions are specific to setting up a build for integration
with Kitware's gitlab server rather than github.  Briefly, the setup procedure
is as follows:

- Install the python [requirements](buildbot-server/requirements.txt)
- Generate a password for the buildbot web interface
```
htpasswd -c webstatuspasswords some-username
```
- Create a secrets file in `/path/to/buildbot-server/secrets.json`
```javascript
{
    "buildbot_root": "/path/to/buildbot-server",
    "web_status_url": "http://this-servers-hostname",
    "web_status_port": 8010, // or some other port to serve the buildbot web interface
    "github_status_token": "authentication token for github with permission to write statuses"
}
```
- Initialize the buildbot sqlite database
```
buildbot create-master /path/to/buildbot-server
```
- Define build slaves as described below
- Start the build master
```
buildbot start /path/to/buildbot-server
```
-  Initialize the slave computer by installing `buildbot-slave==0.8.12` and running
```
buildslave create-slave /path/to/testing/directory buildbot-server-host buildslave-name password
```
The buildslave will contact the buildbot master and initialize itself in the directory
you specified.
-  Start the build slave
```
buildslave start /path/to/testing/directory
```
-  Push a commit to UV-CDAT, you should see it show up in the changes section of the
buildbot web interface and a new build should begin with in a minute or two.
-  Fix the problems you come across that aren't addressed in this readme and
update the instructions so other people don't have the same problems. ;)

Buildbot slave setup
--------------------

On the slave machine, first make sure you can build uvcdat manually, that
will save you a lot of time down the road.  Then you need to define a new
machine definition in [buildbot-server/machines](buildbot-server/machines)
on your buildbot master. (See [buildbot-server/machines/garant](buildbot-server/machines/garant)
for an example).  Create a secrets file containing a user name and password
for the buildbot slave in `buildbot-server/machines/secrets.json` that looks
like this:
```json
{
   "my-machine-name": {
      "password": "my-super-secure-password"
   },
   "my-other-machine-name": {
      "password": "correct horse battery staple"
   }
}
```
Next, you need modify [`buildbot-server/machines/__init__.py`](buildbot-server/machines/__init__.py)
to import your `machine` modules and add them to the `MACHINES` list.  Next you will
need to install the `buildbot-slave==0.8.12` python package on the slave.

Advanced configuration
----------------------

The build and test settings are specified in [buildbot-server/projects/uvcdat](buildbot-server/projects/uvcdat),
different machines can be set up to build different configurations.  The configuration definitions
will need to be added to the uvcdat project module.  This is relatively straightforward because
the buildbot configuration is designed to work with cmake.  See
[buildbot-server/projects/adding_a_project.md](buildbot-server/projects/adding_a_project.md) for
more information.

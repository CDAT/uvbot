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
and run `tangelo -r /path/to/github-proxy` to start the service at `http://localhost:8080/proxy`.  See
`tangelo -h` for more options.

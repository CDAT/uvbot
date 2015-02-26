Kitware buildbot configuration
==============================

This repository hosts the configuration for the buildbot master server.
Currently, it runs on 'hera'. Any changes to this repository will require a
restart of the main server. For now, please contact one of:

  * Ben Boeckel `<ben.boeckel@kitware.com>`
  * Utkarsh Ayachit `<utkarsh.ayachit@kitware.com>`

to restart the server for you.

Testing changes
===============

Changes can be tested locally using buildbot master are is highly recommended
to catch Python errors and other problems. By default, it will poll Gitlab for
merge requests, but not actually write to it. Ensure that your machine and
builds appear in the webpage served by buildbot.

To run the master, a `secrets.json` file will be required. It should look like:

```json
{
    "buildbot_root": "/path/to/dashboardscriptbb/repo",
    "gitlab_rooturl": "https://kwgitlab.kitwarein.com",
    "gitlab_api_token": "myapitoken",
    "web_status_port": 35215
}
```

An API token is availble from your profile page in Gitlab.

Adding a Machine
================

Machines are stored in `machines/`. Each host is a Python module imported by
`machines/__init__.py`.

Complex logic should be avoided in the project descriptions so that changes do
not need to be copied around. Project-specific logic belongs with the project
if possible (additional feature flags may be used to control things). Ideally,
machine/projects descriptions should be purely declarative.

A commented example machine is provided in `machines/_example`.

Don't forget to add your machine to `machines/__init__.py` and send a password
for the machine to one of those listed at the beginning of this file.

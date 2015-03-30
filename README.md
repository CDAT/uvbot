Kitware buildbot configuration
==============================

This repository hosts the configuration for the buildbot master server.
Currently, it runs on 'hera'. Any changes to this repository will require a
restart of the main server. For now, please contact one of:

  * Ben Boeckel `<ben.boeckel@kitware.com>`
  * Utkarsh Ayachit `<utkarsh.ayachit@kitware.com>`

to restart the server for you.

Currently, buildbot 0.8.10 is the preferred version.

Testing changes
===============

Changes can be tested locally using buildbot master are is highly recommended
to catch Python errors and other problems. By default, it will poll Gitlab for
merge requests, but not actually write to it. Ensure that your machine and
builds appear in the webpage served by buildbot.

Create a directory to host the master in with:

```sh
buildbot create-master /path/to/master
```

Create a symlink to the `master.cfg` file from `/path/to/master`. A
`secrets.json` file will be required. It should look like:

```json
{
    "buildbot_root": "/path/to/dashboardscriptbb/repo",
    "gitlab_host": "gitlab.kitware.com",
    "gitlab_api_token": "myapitoken",
    "web_status_url": "http://public_url:port",
    "web_status_port": 35215
}
```

An API token is available from your profile page in Gitlab. Also symlink
`templates` to the directory here. Please note that the bot ignores its own
comments, so you may need to piggyback on another MR to test since you can't
issue `@buildbot test` as the bot (which is you based on your API key).
Finally, to start the master:

```sh
buildbot start /path/to/master
```

In the `buildbot_root` folder, create an htpasswd file named
`webstatuspasswords`. A simple way to do this is with the `htpasswd` command:

```sh
htpasswd -c webstatuspasswords username
```

This sample command will prompt for the password for user `username` and create
the file.

You may set up the `local` machine as needed in `machines/local` and set the
`KW_BUILDBOT_TESTING` environment to use it.

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

It is recommended that machines run buildslave at boot as the correct user so
that after a power outage, things continue to work without human intervention.

Installing buildslave
=====================

Windows
-------

For Windows, the following will be necessary:

  * [Python](https://www.python.org/downloads/release/python-279/)
  * [PyWin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/)
  * [pip](https://pip.pypa.io/en/latest/installing.html)

Once you have these, run:

```batch
> path/to/pip install buildbot-slave==0.8.10
```

This will install the buildslave daemon.

OS X
----

Run:

```sh
$ easy_install install pip
$ pip install virtualenv
$ virtualenv path/to/buildslave/venv
$ path/to/buildslave/venv/bin/pip install buildbot-slave==0.8.10
```

Linux
-----

Install `virtualenv` through the package manager followed by:

```sh
$ virtualenv path/to/buildslave/venv
$ path/to/buildslave/venv/bin/pip install buildbot-slave==0.8.10
```

Setting up buildslave
=====================

Next, run the following:

```sh
$ path/to/buildslave create-slave path/to/buildslave/root hera $machine $password
```

where `$machine` is the name of the machine in this repository (it doesn't need
to match the hostname). Send the password to one of the administrators at the
top of this file.

There will be `info/admin` and `info/host` files which should be filled out.
These will appear on the buildbot web interface.

On Windows, it is recommended to put the buildslave root in a place with a
short path to it. Some projects (e.g., Visual Studio) cannot cope with the long
paths generated by buildbot. See also the `dirlen` keyword argument to the
`projects.make_builders` function to use shorter names for the build
directories.

Running buildslave as a service
===============================

The buildslave service should be set up so that it runs whenever the machine is
restarted. This allows the dashboards to run with a minimum of maintenance when
the power goes out.

Windows
-------

Use Task Manager to set up a service as the user which will run the dashboards.
The important settings:

  * General > Run as the `dashboard` or `kitware` user
  * General > "Run only when user is logged in"
  * Triggers > "At log on" of the user
  * Actions > "Start a program"
    - `path/to/buildslave.bat start path/to/buildslave/root`
  * Settings > **uncheck** "Stop the task if it runs longer than"
  * Settings > "Do not start a new instance" in the last dropdown

The administrator should set it up so that this user is automatically logged in
when the machine reboots:

  * Run `control userpasswords2` and uncheck "Users must enter a user name and
    password to use this computer"
  * Launch "Local Security Policy" as an administrator (found in Control Panel
    > System and Security, click on "Administrative Tools")
  * Under Local Policies > User Rights Assignment, add the user to the "Log on
    as a batch job" policy

OS X
----

OS X uses launchd to run services. The
[LaunchControl](http://www.macupdate.com/app/mac/46921/launchcontrol)
application makes dealing with it easier. Use it to create a task:

  * The command should be `/absolute/path/to/buildslave start path/to/buildslave/root`
  * Save the outputs to files (*StandardErrorPath*)
  * Add *RunAtLoad*
  * Add *ProcessType* to be "Standard"

The user does *not* need to log in automatically.

Linux
-----

Linux has various tools to manage system services. The two main ones are
`systemd` and `sysvinit`.

### systemd

Drop a `buildbot-slave.service` file into
`/etc/systemd/system/default.target.wants` with the contents:

```systemd
[Unit]
Description=Buildbot for dashboards

[Service]
Type=simple
User=kitware

WorkingDirectory=/home/%u
ExecStart=/usr/bin/buildslave start --nodaemon /home/%u/dashboards/buildbot
ExecStop=/usr/bin/buildslave stop /home/%u/dashboards/buildbot

[Install]
WantedBy=multi-user.target
```

Adjust paths, username, etc. as needed. The only restriction is that
`ExecStart=` and `ExecStop=` command lines must start with absolute paths. See
`systemd.unit(5)` and `systemd.exec(5)` for more options which may be required.
For example, `Requires=` and `After=` might be used in the `[Unit]` section to
start up a VNC server for the buildslave.

### sysvinit

Find a script to drop into `/etc/init.d/buildslave` which does the required
incantations. Probably best to copy from an existing one. Once that is done,
run:

```sh
sudo update-rc.d buildslave defaults
```

and hope for the best. Or upgrade to Debian Jessie or Ubuntu 14.10 and use
systemd.

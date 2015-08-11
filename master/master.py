#!/usr/bin/env python

"""Tangelo application that proxy's github events to buildbot."""

import os
import json
import hmac
import hashlib

import tangelo
import requests


# load a projects file
# see https://developer.github.com/webhooks/#events


_projects_file = os.path.join(os.path.dirname(__file__), 'projects.json')
with open(_projects_file) as f:
    projects = json.load(f)['projects']



def authenticate(key, body, received):
    """Authenticate an event from github."""
    print "RECV",received
    computed = hmac.new(str(key), body, hashlib.sha1).hexdigest()
    print "COMP:",computed
    # The folowing func does not exist on my home mac
    # trapping in try/except
    try:
      return hmac.compare_digest(computed, received)
    except:
      return computed == received


def get_project(name):
    """Return the object from `projects` matching `name` or None."""
    return projects.get(name)


def forward(project, obj):
    """Forward an event object to the configured buildbot instance."""
    auth = None
    if project.get('user') and project.get('password'):
        auth = (project['user'], project['password'])

    resp = requests.post(
        project['buildbot'].rstrip('/') + '/change_hook/github',
        data={"payload": obj},
        auth=auth
    )
    #    headers={'CONTENT-TYPE': 'application/x-www-form-urlencoded'}

    if resp.ok:
        print "OK"
        tangelo.http_status(200, 'OK')
        return 'OK'
    else:
        tangelo.http_status(400, "Bad project configuration")
        return 'Bad project configuration'


@tangelo.restful
def get(*arg, **kwarg):
    """Make sure the server is listening."""
    return 'How can I help you?\n'


@tangelo.restful
def post(*arg, **kwarg):
    """Listen for github webhooks, authenticate, and forward to buildbot."""
    # retrieve the headers from the request
    try:
        received = tangelo.request_header('X-Hub-Signature')[5:]
    except Exception:
        received = ''

    # get the request body as a dict
    # for json
    body = tangelo.request_body().read()

    try:
        obj = json.loads(body)
    except:
        tangelo.http_status(400, "Could not load json object")
        return "Could not load json object"

    # obj = json.loads(kwarg['payload'])
    #open('last.json', 'w').write(json.dumps(obj, indent=2))
    project = get_project(obj.get('repository', {}).get('full_name'))
    if project is None:
        tangelo.http_status(400, "Unknown project")
        return 'Unknown project'

    # make sure this is a valid request coming from github
    if not authenticate(project.get('api-key', ''), body, received):
        tangelo.http_status(403, "Invalid signature")
        return 'Invalid signature'

    event = tangelo.request_header('X-Github-Event')
    print "PROJ EVENT:",project["events"],event
    if project['events'] == '*' or event in project['events']:
        obj['event'] = event

        # add a new item to the test queue
        return "Ok sent this to queue"
    else:
        tangelo.http_status(200, "Unhandled event")
        return 'Unhandled event'

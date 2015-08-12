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
    computed = hmac.new(str(key), body, hashlib.sha1).hexdigest()
    # The folowing func does not exist on my home mac
    # trapping in try/except
    try:
      return hmac.compare_digest(computed, received)
    except:
      return computed == received


def get_project(name):
    """Return the object from `projects` matching `name` or None."""
    return projects.get(name)


def forward(slave,obj,signature):
    """Forward an event object to the configured buildbot instance."""

    resp = requests.post(
        slave,
        data=json.dumps(obj),
        headers={"BOT-Signature":"sha1:%s" % signature,
          "BOT-Event":"status",
          }
    )
    #    headers={'CONTENT-TYPE': 'application/x-www-form-urlencoded'}

    return resp


@tangelo.restful
def get(*arg, **kwarg):
    """Make sure the server is listening."""
    return 'How can I help you?\n'


@tangelo.restful
def post(*arg, **kwarg):
    """Listen for github webhooks, authenticate, and forward to buildbot."""
    # retrieve the headers from the request
    print "MASTER RECEIVED A POST EVENT"
    try:
        received = tangelo.request_header('X-Hub-Signature')[5:]
    except Exception:
        try:
            received = tangelo.request_header('BOT-Signature')[5:]
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
    if not authenticate(project.get('api-key', ''), body, received) \
        and \
        not authenticate(project.get('bot-key', ''), body, received):
        tangelo.http_status(403, "Invalid signature")
        return 'Invalid signature'

    event = tangelo.request_header('X-Github-Event')

    print "EVENT:",event
    print "TANGELO BOT",tangelo.request_header('BOT-Event')
    if project['github-events'] == '*' or event in project['github-events']:
        print "BOTKEY:",type(project["bot-key"])
        obj['event'] = event
        signature = hmac.new(str(project["bot-key"]), json.dumps(obj), hashlib.sha1).hexdigest()
        commit = obj["commits"][0]["id"]  # maybe -1 need to test
        print "Commit id:",commit
        nok = 0
        for slave in project["slaves"]:
          print "SENDING TO:",slave
          resp = forward(slave,obj,signature)
          if resp.ok:
            nok+=1

        if nok>0:
          return "Ok sent this to %i slaves out of %i" % (nok,len(project["slaves"]))
        else:
          msg = "All slaves failed, last error was: %s" % resp.text 
          tangelo.http_status(resp.status_code, msg)
          return msg

    elif tangelo.request_header('BOT-Event') == "status":
      ## put here code to update status of commit on github
      print "OK WE GOT A BOT EVENT STATUS"
      headers = {
          "Authorization":"token "+project["token"],
          }
      state = "failure"
      target ="https://open.cdash.org/viewTest.php?buildid=3951103"
      context = "test"
      data = {
          "state":state,
          "target_url": target,
          "description": "running '%s'" % obj["command"],
          "context": context,
          }

      resp = requests.post(
          obj["commit"]["statuses_url"].replace("{sha}",obj["commit"]["id"]),
          data = json.dumps(data),
          headers = headers)

      print "STATUS FORWARD"
      print resp.status_code
      print resp.text
      return "OK RECEIVED A BOT status update EVENT"
    else:
        tangelo.http_status(200, "Unhandled event")
        return 'Unhandled event'

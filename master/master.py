#!/usr/bin/env python

"""Tangelo application that proxy's github events to buildbot."""

import os
import json
import hmac
import hashlib

import tangelo
import requests

import time

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
    print "WE COME IN GET"
    if len(arg)>0:
      try:
        project = get_project("%s/%s" % arg[1:3])
        pth = os.path.join(*arg)
        pth = os.path.join(project["logs_dir"],pth)
        f=open(pth)
        msg = f.read()
        f.close()
      except Exception,err:
        msg = 'How can I help you?\n%s,%s\n%s' % (arg,kwarg,err)
    else:
      msg = 'How can I help you?\n'
    tangelo.content_type("text/html")
    return msg


@tangelo.restful
def post(*arg, **kwarg):
    """Listen for github webhooks, authenticate, and forward to buildbot."""
    # retrieve the headers from the request
    print "MASTER RECEIVED A POST EVENT"
    print "TGELO CONFI",tangelo.cherrypy.request.header_list
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
    project_name = obj.get('repository', {}).get('full_name')
    project = get_project(project_name)
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

    if project['github-events'] == '*' or event in project['github-events']:
        obj['event'] = event
        signature = hmac.new(str(project["bot-key"]), json.dumps(obj), hashlib.sha1).hexdigest()
        commit_id = obj["commits"][0]["id"]  # maybe -1 need to test
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
      headers = {
          "Authorization":"token "+project["token"],
          }
      commit_id = obj["commit"]["id"]
      if obj["code"] == 0:
        state = "success"
      elif obj["code"] is None:
        state = "pending"
      else:
        state = "failure"
      if obj["code"]!=0 and obj["command"].find("ccccccctest")>-1:
        #Ctest has its own special url where it post things
        target ="https://open.cdash.org/viewTest.php?buildid=3951103"
      else:
        slave = obj["slave_host"]
        pth = os.path.join(project["logs_dir"],slave,project_name,commit_id)
        print "DUMPING INFO IN:",pth
        if not os.path.exists(pth):
          os.makedirs(pth)
        f=open(os.path.join(pth,cmd2str(obj["command"])),"w")
        print >>f,"<html><body>"
        print >>f,"<h1>%s (%s)</h1><br><h2>commit: %s<h2>" % (project_name,obj["slave_name"],commit_id)
        host = tangelo.cherrypy.url()
        host=host[host.find("//")+2:]
        if obj["previous"] is not None:
          ptarget = "http://%s/%s/%s/%s/%s" % (host,slave,project_name,commit_id,cmd2str(obj["previous"]))
          print >>f, "<h2>PREVIOUS COMMAND</h2>"
          print >>f,"<a href='%s'>" % ptarget,obj["previous"],"</a>"
        print >>f, "<h2>COMMAND</h2>"
        print >>f,"<pre>",obj["command"],"</pre>"
        print >>f, "<h3>OUTPUT</h3>"
        print >>f,"<pre>",obj["output"],"</pre>"
        print >>f, "<h3>ERROR</h3>"
        print >>f,"<pre>",obj["error"],"</pre>"
        print >>f,"</body></html>"
        f.close()
        target = "http://%s/%s/%s/%s/%s" % (host,slave,project_name,commit_id,cmd2str(obj["command"]))

      context = "cont-int/LLNL/%s-%s" % (obj["os"],obj["slave_name"])
      data = {
          "state":state,
          "target_url": target,
          "description": "running '%s' (%s)" % (obj["command"],time.asctime()),
          "context": context,
          }
      resp = requests.post(
          obj["commit"]["statuses_url"].replace("{sha}",obj["commit"]["id"]),
          data = json.dumps(data),
          verify = False,
          headers = headers)

      return "OK RECEIVED A BOT status update EVENT"
    else:
        tangelo.http_status(200, "Unhandled event")
        return 'Unhandled event'


def cmd2str(command):
  return "__".join(command.split()[:3]).replace("/","_")

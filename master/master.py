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
    # print "TGELO CONFI",tangelo.cherrypy.request.header_list
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
    print "EVENT:",event

    if project['github-events'] == '*' or event in project['github-events']:
        obj['event'] = event
        try:
          commit = obj["head_commit"]
          is_commit = True
        except:
          commit = obj["pull_request"]
          is_commit = False
        if commit is None:
          ## no head_Commit trying to see if it's a pull request
          return "Null Head Commit Found, not a PR either skipping"
        if is_commit:
          commit_id = commit["id"]
          commit_msg = commit["message"]
        else:
          ## It 's a PR faking the head_commit/id bits for slaves
          commits_url = commit["commits_url"]
          commit_id = commit["head"]["sha"]
          commit_statuses_url=commit["statuses_url"]
          commit_ref = commit["head"]["ref"]
          resp = requests.get(commits_url,verify=False)
          commit = resp.json()[-1]["commit"]
          commit_msg=commit["message"]
          commit["id"]=commit_id
          obj["ref"]=commit_ref
          commit["statuses_url"]=commit_statuses_url
          obj["head_commit"]=commit
        signature = hmac.new(str(project["bot-key"]), json.dumps(obj), hashlib.sha1).hexdigest()

        if commit_msg.find("##bot##skip-commit")>-1:
            # User requested to not send this commit to bots
            return "Skipped testing commit '%s' at committer request (found string '##bot##skip-commit')"
        nok = 0
        for islave, slave in enumerate(project["slaves"]):
          islaves = commit_msg.find("##bot##skip-slaves")
          if islaves>-1:
            # ok some slaves need skipping
            msg = commit_msg[islaves+18:]
            iend = msg.find("\n")
            msg = msg[:iend].strip().split()
            iskip = False
            for m in msg:
              if slave.find(m)>-1:
                iskip = True
                break
            if iskip:
              print "\033[%im" % (91+islave),"Commit asked to skip:",slave,"\033[0m"
              nok+=1
              continue
          print "\033[%im" % (91+islave),"SENDING TO:",slave,"\033[0m"
          try:
            resp = forward(slave,obj,signature)
            if resp.ok:
              nok+=1
          except:
            print "\033[%im" % (91+islave),"could not connect","\033[0m"
            nok+=1

        if nok>0:
          return "Ok sent this to %i slaves out of %i" % (nok,len(project["slaves"]))
        else:
          msg = "All slaves failed to respond, last error was: %s" % resp.text 
          print msg
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

      slave = obj["slave_host"]
      try:
        islave = project["slaves"].find("http://"+slave)
      except:
        islave = -91  # Turn off styling
      pth = os.path.join(project["logs_dir"],slave,project_name,commit_id)
      print "\033[%im" % (91+islave),"DUMPING INFO IN:",pth,"\033[0m"
      print "\033[%im" % (91+islave),"could not connect","\033[0m"
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
      if obj["command"].find("ctest")>-1:
        print >>f, "<h3>CTEST PAGE</h3>"
        build_name = "%s-%s" % (slave.replace(":",""),commit_id)
        ptarget = "https://open.cdash.org/index.php?compare1=65&filtercount=2&field1=buildname%%2Fstring&project=UV-CDAT&field2=buildstarttime%%2Fdate&value1=%s" % build_name
        print >>f,"<A HREF='%s'>Click here</A>" % ptarget
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

      return "Received and treated a BOT STATUS update event"
    else:
        tangelo.http_status(200, "Unhandled event")
        return 'Unhandled event'


def cmd2str(command):
  return "__".join(command.split()[:3]).replace("/","_")

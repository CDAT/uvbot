#!/usr/bin/env python

"""Tangelo application that proxy's github events to buildbot."""

import os
import json
import hmac
import hashlib

import tangelo
import requests

import Queue
import threading
import subprocess
import shlex
import time
import shutil

# load a projects file
# see https://developer.github.com/webhooks/#events

queue = Queue.Queue()


def process_commit(project,obj):
   commit = obj["commits"][0]  # maybe -1 need to test
   print "processing commit",commit

   ## We need to store the commit api url
   commit["statuses_url"]=obj["repository"]["statuses_url"]
   commit["repo_full_name"]=obj["repository"]["full_name"]
   # First step go to working directory
   work_dir = project["working_directory"]
   if not os.path.exists(work_dir):
     os.makedirs(work_dir)
   os.chdir(work_dir)
   # Second step clone repo if not done already
   git_repo = obj["repository"]["url"].replace("https","git")
   src_dir = git_repo.split("/")[-1]
   src_dir = os.path.join(work_dir,src_dir)
   if not os.path.exists(src_dir):
     if process_command(project,commit,"git clone %s" % git_repo)!=0:
       return
   os.chdir(src_dir)
   # Update repo
   if process_command(project,commit,"git checkout master")!=0: return
   if process_command(project,commit,"git pull")!=0: return
   # Checkout commit to be tested
   if process_command(project,commit,"git checkout %s" % commit["id"])!=0: return
   # Create and go to build dir
   os.chdir(work_dir)
   build_dir = os.path.join(work_dir,"build")
   if os.path.exists(build_dir):
     #shutil.rmtree(build_dir)
     pass
   else:
     os.makedirs(build_dir)
   os.chdir(build_dir)
   # run cmake
   #if process_command(project,commit,"cmake %s %s" % (src_dir,project["cmake_xtra"]))!=0: return
   # run make
   if process_command(project,commit,"make -j %i mydummyimpossiblemake" % project["build_parallel"])!=0: return
   # run ctest
   process_command(project,commit,"ctest -j %i %s -D Experimental" % (project["test_parallel"],project["ctest_xtra"]))

def process_command(project,commit,command):
  print "Executing:",command
  ## Execute command
  p = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err = p.communicate()
  print out,err
  if p.returncode != 0:
    # Ok something went bad...
    print "Something went bad",out,err
    data = json.dumps({
      "output":out,
      "error":err,
      "code":p.returncode,
      "command":command,
      "commit":commit,
      "repository":{"full_name":commit["repo_full_name"]},
      }
      )
    signature = hmac.new(str(project["bot-key"]), data, hashlib.sha1).hexdigest()
    resp = requests.post(project["master"],
        data = data,
        headers={"BOT-Signature":"sha1:%s" % signature,
          "BOT-Event":"status",
          }
        )
  return -p.returncode




def worker():
    while True:
        project, obj = queue.get()
        process_commit(project,obj)
        queue.task_done()

thread = threading.Thread(target=worker)
thread.daemon = True
thread.start()

_projects_file = os.path.join(os.path.dirname(__file__), 'projects.json')
with open(_projects_file) as f:
    projects = json.load(f)['projects']


def authenticate(key, body, received):
    """Authenticate an event from github."""
    computed = hmac.new(str(key), body, hashlib.sha1).hexdigest()
    print "Computed",computed
    print "received:",received
    # The folowing func does not exist on my home mac
    # trapping in try/except
    try:
      return hmac.compare_digest(computed, received)
    except:
      return computed == received


def get_project(name):
    """Return the object from `projects` matching `name` or None."""
    return projects.get(name)


def forward(dest,obj,signature):
    """Forward an event object to the configured buildbot instance."""

    resp = requests.post(
        dest,
        data={"payload": obj},
        headers={"BOT-Signature":"sha1:%s" % signature,
          "BOT-Event":"status",}
    )

    return resp


@tangelo.restful
def get(*arg, **kwarg):
    """Make sure the server is listening."""
    return 'How can I help you?\n'


@tangelo.restful
def post(*arg, **kwarg):
    """Listen for github webhooks, authenticate, and forward to buildbot."""
    # retrieve the headers from the request
    try:
        received = tangelo.request_header('BOT-Signature')[5:]
    except Exception:
        received = ''
    print "BOT SIGN:",received

    # get the request body as a dict
    # for json
    body = tangelo.request_body().read().strip()
    f=open("crap.json","w")
    f.write(body)
    f.close()

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
    if not authenticate(project.get('bot-key', ''), body, received):
        tangelo.http_status(403, "Invalid signature")
        return 'Invalid signature'

    event = tangelo.request_header('BOT-Event')
    if not event != "push":
      tangelo.http_status(200, "Unhandled event")
      return 'Unhandled event'


    commit = obj["commits"][0]["id"]  # maybe -1 need to test
    print "Commit id:",commit
    queue.put([project,obj])
    return "Ok sent commit %s to queue" % commit

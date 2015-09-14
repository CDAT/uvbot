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
   commit = obj["head_commit"]
   print "processing commit",commit

   ## We need to store the commit api url
   commit["statuses_url"]=obj["repository"]["statuses_url"]
   commit["repo_full_name"]=obj["repository"]["full_name"]
   commit["slave_name"]=project["name"]
   commit["slave_host"]=obj["slave_host"]

   cmd = None
   # First step go to working directory
   work_dir = os.path.abspath(project["working_directory"])
   if not os.path.exists(work_dir):
     os.makedirs(work_dir)
   print "CHANGING DIR TO:",work_dir
   os.chdir(work_dir)
   # Second step clone repo if not done already
   git_repo = obj["repository"]["url"]#.replace("https","git")
   src_dir = git_repo.split("/")[-1]
   src_dir = os.path.join(work_dir,src_dir)
   if not os.path.exists(src_dir):
     cmd = "git clone %s" % git_repo
     if process_command(project,commit,cmd,None)!=0:
       return
   print "CHANGING DIR TO:",src_dir
   os.chdir(src_dir)
   # Resets possible changes from previous commit
   previous = cmd
   cmd = "git reset --hard origin/master"
   if process_command(project,commit,cmd,previous)!=0: return
   # Update repo
   previous = cmd
   cmd = "git checkout master"
   if process_command(project,commit,cmd,previous)!=0: return
   previous = cmd
   cmd = "git pull"
   if process_command(project,commit,cmd,previous)!=0: return
   # Checkout commit to be tested
   previous = cmd
   cmd = "git checkout %s" % commit["id"]
   if process_command(project,commit,cmd,previous)!=0: return
   # Merge master in
   if commit["message"].find("##bot##no-merge-master")==-1:
     previous = cmd
     cmd = "git merge --no-ff master --no-commit"
     if process_command(project,commit,cmd,previous)!=0: return
   # Create and go to build dir
   os.chdir(work_dir)
   build_dir = os.path.join(work_dir,"build")
   if os.path.exists(build_dir):
     previous = cmd
     cmd = "rm -rf  %s" % (build_dir)
     if process_command(project,commit,cmd,previous)!=0: return
   os.makedirs(build_dir)
   os.chdir(build_dir)
   # run cmake
   previous = cmd
   build_name = "%s-%s" % (commit["slave_host"],commit["id"])
   cmd = "cmake %s %s -DBUILDNAME=%s" % (src_dir,project["cmake_xtra"],build_name)
   if commit["message"].find("##bot##cmake_xtra")>-1:
     xtra = commit["message"]
     xtra=xtra[xtra.find("##bot##cmake_xtra")+17:]
     xtra=xtra[:xtra.find("\n")]
     cmd+=" "+xtra
   if process_command(project,commit,cmd,previous)!=0: return
   # run make
   previous = cmd
   cmd = "make -j%i" % project["build_parallel"]
   if process_command(project,commit,cmd,previous)!=0: return
   # run ctest
   previous = cmd
   cmd = "ctest -j%i %s -D Experimental" % (project["test_parallel"],project["ctest_xtra"])
   process_command(project,commit,cmd,previous)

def process_command(project,commit,command,previous_command):
  print time.asctime(),"Executing:",command
  if command is None:
    execute = False
    command = "Request put in Queue, queue size is: %i" % queue.qsize()
  else:
    execute = True
  # Lets tell gituhb what we're doing
  data = json.dumps({
    "os":os.uname()[0],
    "slave_name": commit["slave_name"],
    "slave_host": commit["slave_host"],
    "output":"running...",
    "error":"cross your fingers...",
    "code":None,
    "command":command,
    "previous":previous_command,
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
  if not execute:
    return 0
  ## Execute command
  p = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err = p.communicate()
  print out,err
  if p.returncode != 0:
    # Ok something went bad...
    print "Something went bad",out,err
  data = json.dumps({
    "os":os.uname()[0],
    "slave_name": commit["slave_name"],
    "slave_host": commit["slave_host"],
    "output":out,
    "error":err,
    "code":p.returncode,
    "command":command,
    "previous":previous_command,
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
        print "THREAD QSIZE:",queue.qsize()
        tmp = queue.get()
        project,obj = tmp
        print time.asctime(),"STARTING A NEW BUILD ON THIS THREAD"
        process_commit(project,obj)
        queue.task_done()
        print time.asctime(),"DONE, WAITING FOR A BUILD ON THIS THREAD"

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
    print "BOT SIGN:",received,tangelo.request_header("Host")

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


    commit = obj["head_commit"]["id"]
    print "Commit id:",commit
    obj["slave_host"]=tangelo.request_header("Host")
    queue.put([project,obj])
    print "Queue size:",queue.qsize()
    for i in range(queue.qsize()):
        proj,tmpobj = queue.get()
        queue.task_done()
        if proj==project and tmpobj["ref"]==obj["ref"] and tmpobj["head_commit"]["id"]!=obj["head_commit"]["id"]:
            # same proj same branch different commit so the one we are trying to add is more recent
            # no need to test the old one
            print "Deleting old commit (%s) for branch (%s) from queue" % (tmpobj["head_commit"]["id"], tmpobj["ref"])
        else:
            # ok nothing to do with new elt, putting back in queue
            queue.put([proj,tmpobj])
            print "put back in queue"
        print "Queue size in loop:",queue.qsize()
    print "Queue size after loop:",queue.qsize()
    commit = obj["head_commit"]
    print "processing commit",commit

    ## We need to store the commit api url
    commit["statuses_url"]=obj["repository"]["statuses_url"]
    commit["repo_full_name"]=obj["repository"]["full_name"]
    commit["slave_name"]=project["name"]
    commit["slave_host"]=obj["slave_host"]
    process_command(project,commit,None,None)
    return "Ok sent commit %s to queue" % commit

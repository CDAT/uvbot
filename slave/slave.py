#!/usr/bin/env python

"""Tangelo application that proxy's github events to buildbot."""

import os
import json
import hmac
import hashlib

import tangelo
import requests

import Queue
import multiprocessing
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
   commit["original_ref"]=obj["ref"]

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
     if threaded_command(project,commit,cmd,None,work_dir)!=0:
       return
   print "CHANGING DIR TO:",src_dir
   os.chdir(src_dir)
   # Resets possible changes from previous commit
   previous = cmd
   cmd = "git reset --hard origin/master"
   if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   # Resets possible changes from previous commit
   previous = cmd
   cmd = "git checkout -- ."
   if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   # Update repo
   previous = cmd
   cmd = "git checkout master"
   os.chdir(src_dir)
   if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   previous = cmd
   cmd = "git pull"
   os.chdir(src_dir)
   if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   # Checkout commit to be tested
   previous = cmd
   os.chdir(src_dir)
   cmd = "git checkout %s" % commit["id"]
   if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   # Merge master in
   if commit["message"].find("##bot##no-merge-master")==-1:
     previous = cmd
     os.chdir(src_dir)
     cmd = "git merge --no-ff master --no-commit"
     if threaded_command(project,commit,cmd,previous,src_dir)!=0: return
   # Create and go to build dir
   os.chdir(work_dir)
   build_dir = os.path.join(work_dir,"build")
   if os.path.exists(build_dir):
       shutil.rmtree(build_dir, ignore_errors=True)
   os.makedirs(build_dir)
   os.chdir(build_dir)
   # run cmake
   previous = cmd
   build_name = "%s-%s" % (commit["slave_host"],commit["id"])
   cmd = "cmake %s %s -DBUILDNAME=%s" % (src_dir,project["cmake_xtra"],build_name)
   if commit["message"].find("##bot##cmake_xtra")>-1:
     xtra = commit["message"]
     xtra=xtra[xtra.find("##bot##cmake_xtra")+17:]
     xtra=xtra.split("\n")[0]
     cmd+=" "+xtra
   if threaded_command(project,commit,cmd,previous,build_dir)!=0: return
   # run make
   previous = cmd
   cmd = "make -j%i" % project["build_parallel"]
   os.chdir(build_dir)
   if threaded_command(project,commit,cmd,previous,build_dir)!=0: return
   # because of merge master we are in detached head mode
   # the uvcdat-testdata cannot figure out anymore where it came from
   # we need to try to fix this manually
   previous = cmd
   cmd = "git checkout %s" % commit["original_ref"].split("refs/heads/")[-1]
   testdata_dir = os.path.join(build_dir,"uvcdat-testdata")
   os.chdir(testdata_dir)
   threaded_command(project,commit,cmd,previous,testdata_dir,never_fails=True)
   # Merge master in
   if commit["message"].find("##bot##no-merge-master")==-1:
     previous = cmd
     os.chdir(testdata_dir)
     # CMake does not checkout the whole history, this can lead to conflict
     # with merge command bellow
     cmd = "git fetch --depth=10"
     if threaded_command(project,commit,cmd,previous,testdata_dir)!=0: return
     previous = cmd
     # for pictures we want ff or it thinks conflicts everywhwrre
     cmd = "git merge master --no-commit"
     if threaded_command(project,commit,cmd,previous,testdata_dir)!=0: return
   # run ctest
   previous = cmd
   cmd = "ctest -j%i %s -D Experimental" % (project["test_parallel"],project["ctest_xtra"])
   os.chdir(build_dir)
   threaded_command(project,commit,cmd,previous,build_dir)

def threaded_command(project,commit,command,previous_command,cwd,never_fails=False):
    P2 = multiprocessing.Process(target=process_command,
        args = (project,commit,command,previous_command,cwd,never_fails))
    time_start = time.time()
    result_filename = os.path.join(project["working_directory"],"build","output_%s" % commit["id"])
    if os.path.exists(result_filename):
        os.remove(result_filename)
    P2.start()
    while P2.is_alive() and time.time()-time_start<project.get("timeout",14400):
      time.sleep(5)
    if P2.is_alive():  # timed out
      print "Process still alive!"
      print "Timed out job"
      talk_to_master(project,commit,"running...","Timed out",-1,command,previous_command)
      P2.terminate()
      ret = -1
      print "killed job"
    else:
      if os.path.exists(result_filename):
          print "result file is here"
          f=open(result_filename)
          ret = int(f.read())
          f.close()
      else:
          print "OHOH! No result file, assuming failure"
          ret = -1
      print "GOT BACK OUT:",ret
    print "SENDING BACK:",ret
    if os.path.exists(result_filename):
        os.remove(result_filename)
    return ret

def process_command(project,commit,command,previous_command,cwd,never_fails=False):
  print time.asctime(),"Executing:",command
  if command is None:
    execute = False
    command = "In Queue: %i" % queue.qsize()
  else:
    execute = True
  # Lets tell gituhb what we're doing
  talk_to_master(project,commit,"running...","cross your fingers...",None,command,previous_command)
  result_filename = os.path.join(project["working_directory"],"build","output_%s" % commit["id"])

  if not execute:
    f=open(result_filename,"w")
    print >>f, 0
    f.close()
    return 0
  ## Execute command
  print "IN PROCESS COMMAND:",os.getcwd()
  p = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd)
  out,err = p.communicate()
  print out,err
  if never_fails:
    p.return_code=0
  if p.returncode != 0:
    # Ok something went bad...
    print "Something went bad",out,err
  talk_to_master(project,commit,out,err,p.returncode,command,previous_command)
  f=open(result_filename,"w")
  print >>f, -p.returncode
  f.close()
  return -p.returncode


def talk_to_master(project,commit,out,err,code,command,previous_command):
  data = json.dumps({
    "os":os.uname()[0],
    "slave_name": commit["slave_name"],
    "slave_host": commit["slave_host"],
    "output":out,
    "error":err,
    "code":code,
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
  return resp


def worker():
    print "In worker b4 while true"
    while True:
        print "THREAD QSIZE:",queue.qsize()
        tmp = queue.get()
        project,obj = tmp
        print time.asctime(),"STARTING A NEW BUILD ON THIS THREAD"
        P = multiprocessing.Process(target=process_commit,args=(project,obj))
        P.start()
        start_time= time.time()
        while P.is_alive():
            time.sleep(5)
        queue.task_done()
        print time.asctime(),"DONE, WAITING FOR A BUILD ON THIS THREAD"


_projects_file = os.path.join(os.path.dirname(__file__), 'projects.json')
with open(_projects_file) as f:
    projects = json.load(f)['projects']

print "in main area starting worker"
process = threading.Thread(target=worker)
process.daemon = True
process.start()

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
    commit["original_ref"]=obj["ref"]
    commit["slave_name"]=project["name"]
    commit["slave_host"]=obj["slave_host"]
    process_command(project,commit,None,None,None)
    return "Ok sent commit %s to queue" % commit

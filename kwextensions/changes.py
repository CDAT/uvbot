from buildbot.changes import base
from buildbot.util.state import StateMixin
from buildbot import config
from twisted.python import log
from twisted.internet import defer

import gitlab
import urllib
from dateutil.parser import parse as dateparse
import datetime
import os
import requests
import json

GUEST     = 10
REPORTER  = 20
DEVELOPER = 30
MASTER    = 40
OWNER     = 50

class Gitlab(gitlab.Gitlab):
    def getsortedmergerequests(self, project_id, page=1, per_page=20, state=None):
        """Returns merge requests sorted in descending order by update time"""
        data = {'page': page, 'per_page': per_page, 'state': state,
                'order_by': 'updated_at', 'sort': 'desc' }

        request = requests.get('{}/{}/merge_requests'.format(self.projects_url, project_id),
                               params=data, headers=self.headers, verify=self.verify_ssl)
        if request.status_code == 200:
            return json.loads(request.content.decode("utf-8"))
        else:
            return False

    def getprojectteammember(self, project_id, user_id):
        """
        Gets a project's team member's information.

        @param project_id (required) - The ID or NAMESPACE/PROJECT_NAME of a project
        @param user_id (required) - The ID of a user
        {
          "id": 1,
          "username": "john_smith",
          "email": "john@example.com",
          "name": "John Smith",
          "state": "active",
          "created_at": "2012-05-23T08:00:58Z",
          "access_level": 40
        }
        """
        request = requests.get("{}/{}/members/{}".format(self.projects_url, project_id, user_id),
                params={}, headers=self.headers,
                verify=self.verify_ssl)
        if request.status_code == 200:
            return json.loads(request.content.decode("utf-8"))
        else:
            return False

    def getgroupmembers(self, group_id):
        """
        Get a list of group members viewable by the authenticated user.
        @param group_id: The group ID.

        @return
        [
          {
            "id": 1,
            "username": "raymond_smith",
            "email": "ray@smith.org",
            "name": "Raymond Smith",
            "state": "active",
            "created_at": "2012-10-22T14:13:35Z",
            "access_level": 30
          },
          {
            "id": 2,
            "username": "john_doe",
            "email": "joh@doe.org",
            "name": "John Doe",
            "state": "active",
            "created_at": "2012-10-22T14:13:35Z",
            "access_level": 30
          }
        ]
        """
        request = requests.get("{}/{}/members".format(self.groups_url, group_id),
                params={}, headers=self.headers,
                verify=self.verify_ssl)
        if request.status_code == 200:
            return json.loads(request.content.decode("utf-8"))
        else:
            return False

    def getaccesslevel(self, project_id, user_id):
        """Returns the access level for a user with respect to a particular
        project

        @param project_id (required) - The ID or NAMESPACE/PROJECT_NAME of a project
        @param user_id (required) - The ID of a user
        """
        pm = self.getprojectteammember(project_id, user_id)
        if pm:
            return int(pm["access_level"])

        project = self.getproject(project_id)
        if project and project.has_key("namespace"):
            members = self.getgroupmembers(project["namespace"]["id"])
            if not members: return 0
            for m in members:
                if m["id"] == user_id: return int(m["access_level"])
        return 0

class GitlabMergeRequestPoller(base.PollingChangeSource, StateMixin):
    compare_attrs = ["rooturl", "token", "projects"]

    def __init__(self, rooturl, token, projects=[], verify_ssl=False, **kwargs):
        """
        @param rooturl: URL to the gitlab server e.g. https://kwgitlab.kitwarein.com
        @type rooturl: string

        @param token: secret token to access Gitlab API.

        @param projects: list of fully qualifies projects names to
        monitor e.g. ["ParaView/ParaView", "utkarsh.ayachit/WonderfulProject"]

        """
        base.PollingChangeSource.__init__(self,
                name="GitlabMergeRequestPoller(%s)" % rooturl, **kwargs)

        self.rooturl = rooturl
        self.token = token
        self.projects = projects
        self.verify_ssl = verify_ssl
        self.api = None
        self.lastRev = {}

    def startService(self):
        self.api = Gitlab(self.rooturl, token=self.token, verify_ssl=self.verify_ssl)
        if not self.api.currentuser():
            log.err("while initializing GitlabMergeRequestPoller for" + self.rooturl)
        else:
            d = self.getState('lastRev', {})
            def setLastRev(lastRev):
                pass
                # FIXME: remove this once we want to rememember between restarts
                self.lastRev = lastRev
            d.addCallback(setLastRev)
            d.addCallback(lambda _:
                    base.PollingChangeSource.startService(self))
            d.addErrback(log.err, 'while initializing GitPoller repository')
            return d

    def describe(self):
        str = ('GitlabMergeRequestPoller watching the remote git repository ' + self.rooturl)
        if self.projects:
            if not callable(self.projects):
                str += ', projects: ' + ', '.join(self.projects)
        if not self.master:
            str += " [STOPPED - check log]"
        return str

    @defer.inlineCallbacks
    def poll(self):
        "Iterate over all projects and poll them"
        log.msg("Polling .................. ")
        for project in self.projects:
            projectid = urllib.quote(project.lower(),"")
            yield self._poll_project(projectid, project)
        log.msg("Done polling")
        yield self.setState('lastRev', self.lastRev)

    @defer.inlineCallbacks
    def _poll_project(self, projectid, projectname):
        # scan through open merge requests.
        # - any merge request with 'request-builds' label will be authorized and
        # scheduled for a build. We also remove the 'request-builds' label.
        openmergerequests = self.api.getsortedmergerequests(projectid,
                page=1, per_page=100, state='opened')
        for mr in openmergerequests:
            mid = mr["id"]
            if 'do-tests' in mr["labels"]:
                if self._authenticate_merge_request(mr):
                    branch = self.api.getbranch(mr["source_project_id"], mr["source_branch"])
                    sha = branch["commit"]["id"]
                    # check if the merge request has updated since the last we
                    # saw it.
                    if self.lastRev.get(unicode(mid), None) != unicode(sha):
                        self.lastRev[unicode(mid)] = unicode(sha)
                        self._accept_change(mr)
                        yield self._add_change(projectname, mr, branch['commit'])
                else:
                    self._reject_change(mr)

    def _authenticate_merge_request(self, mr):
        if 'KW_BUILDBOT_PRODUCTION' not in os.environ:
            return False
        project_id = mr["project_id"]
        access_level = self.api.getaccesslevel(project_id, mr["author"]["id"])
        if access_level >= DEVELOPER:
            log.msg("Merge request is created by a 'developer'")
            return True
        # Since the merge request creator is not a developer. We need to look at the
        # comments to see if an authorized user said "enable-tests".
        comments = self.api.getmergerequestcomments(project_id, mr["id"], page=1, per_page=2000)
        for comment in comments:
            if comment["note"].find(":+1") != -1 and \
                    self.api.getaccesslevel(project_id, comment["author"]["id"]) >= DEVELOPER:
                log.msg("Merge request was not-created by a 'developer' but has a developer +1")
                return True
        log.msg("Merge request was not-created by a 'developer' nor has no +1")
        return False

    def _accept_change(self, mr):
        self.api.createmergerequestewallnote(mr["project_id"], mr["id"],
                "**BUILDBOT**:Will schedule builds soon." \
                "You can monitor the status [here](http://hera:8010/grid?%s)" % \
                        urllib.urlencode({'branch': mr['source_branch']}))

    def _reject_change(self, mr):
        #self.api.createmergerequestewallnote(mr["project_id"], mr["id"],
        #        "BUILDBOT: Builds not authorized! Contact a developer!!! :-1:")
        pass

    @defer.inlineCallbacks
    def _add_change(self, projectname, mr, commit):
        source_project = self.api.getproject(mr["source_project_id"])

        yield self.master.addChange(
                author = "%s <%s>" % (commit["author_name"], commit["author_email"]),
                revision = commit["id"],
                revlink = "%s/commit/%s" % (source_project['web_url'], commit['id']),
                comments = mr["title"] + "\n\n" + mr["description"],
                files = ["--coming soon--"],
                category="merge-request",
                # FIXME: add an option to simply use current timestamp
                when_timestamp = datetime.datetime.now(), # dateparse(commit["authored_date"]),
                branch = mr["source_branch"],
                project = projectname,
                repository = source_project["http_url_to_repo"],
                src = "gitlab",
                properties = {
                    'source_repo' : source_project["http_url_to_repo"],
                    'source_project_id' : mr['source_project_id'],
                    'source_branch' : mr['source_branch'],
                    'merge_request_id' : mr['id'],
                    'target_project_id' : mr['target_project_id'],
                    'rooturl' : self.rooturl
                    }
                )


class GitlabIntegrationBranchPoller(base.PollingChangeSource, StateMixin):
    """
    Polls integration branches for changes and tests them.
    """
    compare_attrs = ["rooturl", "token", "projects"]

    def __init__(self, rooturl, token, projects={}, verify_ssl=False, **kwargs):
        """
        @param rooturl: URL to the gitlab server e.g. https://kwgitlab.kitwarein.com
        @type rooturl: string

        @param token: secret token to access Gitlab API.

        @param projects: dict of fully qualifies projects names with a list of branches
        to monitor e.g. {
            "ParaView/ParaView" : ["master", "next"],
            "utkarsh.ayachit/WonderfulProject" : ["master"]
        }
        """
        base.PollingChangeSource.__init__(self,
                name="GitlabIntegrationBranchPoller(%s)"%rooturl, **kwargs)

        self.rooturl = rooturl
        self.token = token
        self.projects = projects
        self.verify_ssl = verify_ssl
        self.api = None
        self.lastRev = {}

    def startService(self):
        self.api = Gitlab(self.rooturl, token=self.token, verify_ssl=self.verify_ssl)
        if not self.api.currentuser():
            log.err("while initializing GitlabIntegrationBranchPoller for" + self.rooturl)
        else:
            d = self.getState('lastRev', {})
            def setLastRev(lastRev):
                pass
                # FIXME: remove this once we want to rememember between restarts
                self.lastRev = lastRev
            d.addCallback(setLastRev)
            d.addCallback(lambda _:
                    base.PollingChangeSource.startService(self))
            d.addErrback(log.err, 'while initializing GitPoller repository')
            return d

    def describe(self):
        txt = ('GitlabIntegrationBranchPoller watching the remote git repository ' + self.rooturl)
        if self.projects:
            if not callable(self.projects):
                txt += ', projects: ' + str(self.projects)
        if not self.master:
            txt += " [STOPPED - check log]"
        return txt

    @defer.inlineCallbacks
    def poll(self):
        "Iterate over all projects and poll them"
        log.msg("Polling .................. ")
        for project, branches in self.projects.iteritems():
            projectid = urllib.quote(project.lower(),"")
            yield self._poll_project(projectid, project, branches)
        log.msg("Done polling")
        yield self.setState('lastRev', self.lastRev)

    @defer.inlineCallbacks
    def _poll_project(self, projectid, projectname, branches):
        for branchname in branches:
            branch = self.api.getbranch(projectid, branchname)
            if not branch:
                log.err("No such branch %s:%s" % (projectname, branch))
                continue
            commit = branch["commit"]
            sha = commit["id"]
            # check if the branch has updated since the last we saw it.
            key = unicode("%s.%s" % (projectid, branchname))
            sha = unicode(sha)

            project = self.api.getproject(projectid)

            if self.lastRev.get(key, None) != sha:
                self.lastRev[key] = sha
                # TODO: should we do builds for each merge of just the latest state?
                yield self.master.addChange(
                        author = "%s <%s>" % (commit["author_name"], commit["author_email"]),
                        revision = commit["id"],
                        comments = commit["message"],
                        files = ["--coming soon--"],
                        category="integration-branch",
                        # FIXME: add an option to simply use current timestamp
                        when_timestamp = datetime.datetime.now(), # dateparse(commit["authored_date"]),
                        branch = branchname,
                        project = projectname,
                        repository = project["http_url_to_repo"],
                        src="gitlab",
                        properties= {
                            'source_repo' : project["http_url_to_repo"],
                            'rooturl' : self.rooturl
                        })

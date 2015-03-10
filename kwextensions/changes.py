from buildbot.changes import base
from buildbot.util.state import StateMixin
from buildbot import config
from twisted.python import log
from twisted.internet import defer

import urllib
from dateutil.parser import parse as dateparse
import datetime
import os
import requests

GUEST     = 10
REPORTER  = 20
DEVELOPER = 30
MASTER    = 40
OWNER     = 50


def _mkrequest(path, **defkwargs):
    def func(self, *args, **kwargs):
        data = defkwargs.copy()
        data.update(kwargs)

        return self.fetch(path.format(*args), **data)

    return func


def _mkrequest_paged(path, **defkwargs):
    def func(self, *args, **kwargs):
        data = defkwargs.copy()
        data.update(kwargs)

        return self.fetch_all(path.format(*args), **data)

    return func


def _mkpost(path, **defkwargs):
    def func(self, *args, **kwargs):
        data = defkwargs.copy()
        data.update(kwargs)

        return self.post(path.format(*args), **data)

    return func


class Gitlab(object):
    def __init__(self, host, token, verify_ssl=True):
        self.urlbase = 'https://%s/api/v3' % host
        self.headers = {
            'PRIVATE-TOKEN': token,
        }
        self.verify_ssl = verify_ssl

    def fetch(self, path, **kwargs):
        url = '%s/%s' % (self.urlbase, path)
        response = requests.get(url, headers=self.headers, verify=self.verify_ssl, **kwargs)

        if response.status_code != 200:
            return False

        if callable(response.json):
            return response.json()
        else:
            return response.json

    def fetch_all(self, path, **kwargs):
        kwargs.update({
            'page': 1,
            'per_page': 100,
        })

        full = []
        while True:
            items = self.fetch(path, params=kwargs)
            if not items:
                break
            full += items
            if len(items) < kwargs['per_page']:
                break
            kwargs['page'] += 1

        return full

    def post(self, path, **kwargs):
        url = '%s/%s' % (self.urlbase, path)
        response = requests.post(url, headers=self.headers, verify=self.verify_ssl, data=kwargs)

        if response.status_code != 201:
            return False

        if callable(response.json):
            return response.json()
        else:
            return response.json

    # Users
    currentuser = _mkrequest('user')

    # Projects
    getproject = _mkrequest('projects/{}')
    getprojects = _mkrequest_paged('projects')
    getprojectmembers = _mkrequest_paged('projects/{}/members')
    getprojectteammember = _mkrequest('projects/{}/members/{}')
    getbranch = _mkrequest('projects/{}/repository/branches/{}')

    # Merge requests
    getmergerequests = _mkrequest_paged('projects/{}/merge_requests')
    getsortedmergerequests = _mkrequest_paged('projects/{}/merge_requests',
        order_by='updated_at',
        sort='desc')
    getmergerequestcomments = _mkrequest_paged('projects/{}/merge_request/{}/comments')
    createmergerequestwallnote = _mkpost('projects/{}/merge_requests/{}/notes')

    # Groups
    getgroupmembers = _mkrequest_paged('groups/{}/members')

    def getaccesslevel(self, project_id, user_id):
        members = self.getprojectmembers(project_id)

        project = self.getproject(project_id)
        if project and 'namespace' in project:
            group_members = self.getgroupmembers(project['namespace']['id'])
            members += group_members

        access = 0
        for perm in filter(lambda member: user_id == member['id'], members):
            if perm['access_level'] > access:
                access = perm['access_level']
        return access


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
                state='opened')
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
                body="**BUILDBOT**: Your merge request has been queued for testing. " \
                     "You can monitor the status [here](http://hera:8010/grid?%s)." % \
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
                    'source_project_id' : mr['source_project_id'],
                    'source_branch' : mr['source_branch'],
                    'merge_request_id' : mr['id'],
                    'target_project_id' : mr['target_project_id'],
                    'rooturl' : self.rooturl,
                    'try_user_fork' : True,
                    'owner' : source_project['owner']['username']
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
                            'rooturl' : self.rooturl,
                            'try_user_fork' : False
                        })

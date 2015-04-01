from buildbot.changes import base
from buildbot.util.state import StateMixin
from buildbot import config
from twisted.python import log
from twisted.internet import defer

import urllib
from dateutil.parser import parse as dateparse
from datetime import datetime, timedelta
from operator import itemgetter
import os
import re
import requests

import cdash
import trailers

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
        response = requests.get(url, headers=self.headers, verify=self.verify_ssl, params=kwargs)

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
            items = self.fetch(path, **kwargs)
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
    getusers = _mkrequest_paged('users')
    getuser = _mkrequest_paged('users/{}')

    # Projects
    getproject = _mkrequest('projects/{}')
    getprojects = _mkrequest_paged('projects')
    getprojectmembers = _mkrequest_paged('projects/{}/members')
    getprojectteammember = _mkrequest('projects/{}/members/{}')
    getbranch = _mkrequest('projects/{}/repository/branches/{}')

    # Merge requests
    getmergerequests = _mkrequest_paged('projects/{}/merge_requests')
    getmergerequest = _mkrequest('projects/{}/merge_request/{}')
    getsortedmergerequests = _mkrequest_paged('projects/{}/merge_requests',
        order_by='updated_at',
        sort='desc')
    getmergerequestcomments = _mkrequest_paged('projects/{}/merge_request/{}/comments')
    getmergerequestwallnotes = _mkrequest_paged('projects/{}/merge_requests/{}/notes')
    getmergerequestchanges = _mkrequest('projects/{}/merge_request/{}/changes')
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

    def getaccesslevel_cache(self, cache, project_id, user_id):
        key = '%d,%d' % (project_id, user_id)
        if key not in cache:
            cache[key] = self.getaccesslevel(project_id, user_id)
        return cache[key]


class GitlabPoller(base.PollingChangeSource, StateMixin):
    compare_attrs = [
        'host',
        'token',
    ]

    def __init__(self, name, host, token, verify_ssl=False, **kwargs):
        base.PollingChangeSource.__init__(self, name=name % host, **kwargs)

        self.host = host
        self.token = token
        self.verify_ssl = verify_ssl
        self.api = None
        self.last_rev = {}
        self.last_poll_time = None

    def set_last_rev(self, lastRev):
        """Called to set the lastRev state loaded when session is restarted."""
        self.last_rev = lastRev

    def startService(self):
        self.api = Gitlab(self.host, token=self.token, verify_ssl=self.verify_ssl)
        buildbot_user = self.api.currentuser()
        if not buildbot_user:
            log.err('cannot connect to gitlab instance %s' % self.host)
        else:
            self.buildbot_id = buildbot_user['id']
            d = self.getState('lastRev', {})
            me = self
            def _set_last_rev(last_rev):
                me.set_last_rev(last_rev)
            d.addCallback(_set_last_rev)
            d.addCallback(lambda _: base.PollingChangeSource.startService(self))
            d.addErrback(log.err, 'cannot initialize GitlabPoller')
            return d

    def describe_files(self, files):
        descs = []
        for file_desc in files:
            if file_desc['new_file']:
                descs.append('Added %(new_path)s' % file_desc)
            elif file_desc['deleted_file']:
                descs.append('Deleted %(old_path)s' % file_desc)
            elif file_desc['renamed_file']:
                descs.append('Renamed %(old_path)s -> %(new_path)s' % file_desc)
            else:
                descs.append('Changed %(old_path)s' % file_desc)
        return descs

    def describe(self):
        msg = self.name
        if not self.master:
            msg += ' [**STOPPED** --- check logs]'
        if self.last_poll_time is not None:
            msg += ' [Last polled: %s]' % self.last_poll_time.strftime('%c')
        return msg

    def safe_now(self):
        # Allow slaves to be up to 5 minutes behind the master.
        return datetime.now() - timedelta(seconds=5 * 60)


class GitlabMergeRequestPoller(GitlabPoller):
    compare_attrs = [
        'web_host',
        'projects',
        'cdash_info',
    ]

    # TODO: add options for required access level.
    def __init__(self, host, token, web_host, projects=[], cdash_info={}, **kwargs):
        GitlabPoller.__init__(self, 'GitlabMergeRequestPoller(%s)', host, token, **kwargs)

        self.web_host = web_host
        self.projects = projects
        self.cdash_info = cdash_info

        # Special comment regular expressions.
        self._branch_update_re = re.compile('^Added [1-9][0-9]* new commits?:\n\n(\* [0-9a-f]* - [^\n]*\n)*$')

        self._BUILDBOT_PREFIX = '@buildbot '

    def describe(self):
        msg = GitlabPoller.describe(self)
        if self.projects:
            msg += ' (%s)' % ', '.join(self.projects)
        return msg

    def set_last_rev(self, lastRev):
        """Called to set the lastRev state loaded when session is restarted.
        Overridden to support versions.
        v1: { u'$MR-id' : u'$SHA', ... }
        v2: { u'__version__': 2.0, u'$MR-id': {u'$cmd' : u'$SHA', ..}, ...}
        """
        version = float(lastRev.get(u'__version__', 1.0))
        if version < 2.0:
            # v1 only supported 'test' command. So converting to v2 is easy!
            newLastRev = {}
            for key, value in lastRev.iteritems():
                newLastRev[key] = {u'test' : value}
            lastRev = newLastRev
        lastRev[u'__version__'] = 2.0
        GitlabPoller.set_last_rev(self, lastRev)

    @defer.inlineCallbacks
    def poll(self):
        self.last_poll_time = datetime.now()
        for project in self.projects:
            pid = urllib.quote(project.lower(), '')
            yield self._poll_project(pid, project)
        yield self.setState('lastRev', self.last_rev)

    @defer.inlineCallbacks
    def _poll_project(self, pid, project):
        requests = self.api.getsortedmergerequests(pid, state='opened')
        for request in requests:
            mid = request['id']
            branch = self.api.getbranch(request['source_project_id'], request['source_branch'])

            if not branch:
                # Branch is not accessible.
                continue

            commit = branch['commit']

            command_set = self._check_merge_request(request, commit)
            if command_set:
                sha = commit['id']
                unicodesha = unicode(sha)

                # we'll keep last revs for each command separately for each MR.
                last_revs_for_mr = self.last_rev.get(unicode(mid), {})

                # filter command set to only issue those that are new
                # for the commit.
                command_list = [cmd for cmd in command_set \
                        if last_revs_for_mr.get(unicode(cmd)) != unicodesha ]

                if command_list:
                    # TODO: cancel previous builds for this branch if they exist.

                    # update last_revs_for_mr for the commands being issued.
                    for cmd in command_list:
                        last_revs_for_mr[unicode(cmd)] = unicodesha
                    self.last_rev[unicode(mid)] = last_revs_for_mr
                    self._accept_change(request, commit, project)
                    yield self._add_change(project, request, commit, command_list)
            else:
                self._reject_change(request)

    def _strip_prefix(self, string, prefix):
        return string[len(prefix):]

    # TODO: return an action
    def _check_merge_request(self, request, commit):
        pid = request['target_project_id']
        access_cache = {}

        # Look at comments for buildbot commands.
        comments = self.api.getmergerequestwallnotes(pid, request['id'])

        # Sort comments from newest to oldest.
        comments.sort(key=itemgetter('id'), reverse=True)

        # authorized commands.
        commands = set()

        for comment in comments:
            body = comment['body']

            if 'editable' in comment and not comment['editable']:
                if self._branch_update_re.match(body):
                    # TODO: use when receiving webhook notification.
                    branch_update_found = True
                # Ignore non-user comments.
                continue

            author = comment['author']
            if author['id'] == self.buildbot_id:
                cur_trailers = trailers.parse(body)

                trailer_dict = {}
                for key, value in cur_trailers:
                    trailer_dict[key] = value

                if trailer_dict.get('Branch-at') == commit['id']:
                    # Comment is a scheduled build; don't look before this
                    # comment.
                    break

                # Skip comments by buildbot.
                continue

            commands_in_comment = set()
            content = body.splitlines()
            for line in content:
                if line.startswith(self._BUILDBOT_PREFIX):
                    for acommand in line.split()[1:]:
                        # XXX: Add buildbot commands here.
                        if acommand in ['test', 'superbuild']:
                            commands_in_comment.add(acommand)
                        else:
                            # TODO: mention that the command is not recognized?
                            pass

            # add authorized commands to the 'commands' set.
            if commands_in_comment and \
                    self.api.getaccesslevel_cache(access_cache, pid, author['id']) >= DEVELOPER:
                        commands.update(commands_in_comment)

        return commands

    def _accept_change(self, request, commit, project):
        msg = '**BUILDBOT**: Your merge request has been queued for testing.'

        # Add a link to CDash for test results.
        if project in self.cdash_info:
            (cdash_host, cdash_project) = self.cdash_info[project]
            q = cdash.Query(cdash_project)
            q.add_filter(('buildname/string', cdash.StringOp.CONTAINS, commit['id'][:8]))
            q.add_filter(('buildstarttime/date', cdash.DateOp.IS_AFTER, datetime.now()))
            msg += ' You may view the test results [here](%s).' % q.get_url('%s/index.php' % cdash_host)

        project_info = self.api.getproject(request['project_id'])

        # TODO: How to handle branches with the same name over time?
        msg += ' Kitware developers may monitor the status of testing [here](%s/grid?%s).' % (
            self.web_host,
            urllib.urlencode((
                ('branch', request['source_branch']),
                ('category', '%s-expected' % project_info['path']),
                ('category', '%s-exotic' % project_info['path']),
            )),
        )

        msg += '\n\n%s%s' % (trailers.BRANCH_HEAD_PREFIX, commit['id'])

        if 'KW_BUILDBOT_PRODUCTION' not in os.environ:
            log.msg('would accept change %d:\n\n%s' % (request['id'], msg))
            return

        self.api.createmergerequestwallnote(request['project_id'], request['id'], body=msg)

    def _reject_change(self, request):
        if 'KW_BUILDBOT_PRODUCTION' not in os.environ:
            log.msg('would reject change %d' % request['id'])
            return
        # TODO: Make a comment?
        pass

    @defer.inlineCallbacks
    def _add_change(self, project, request, commit, command_list):
        source_project_info = self.api.getproject(request['source_project_id'])
        target_project_info = self.api.getproject(request['target_project_id'])

        changes = self.api.getmergerequestchanges(target_project_info['id'], request['id'])

        yield self.master.addChange(
            author='%(author_name)s <%(author_email)s>' % commit,
            revision=commit['id'],
            revlink='%s/commit/%s' % (source_project_info['web_url'], commit['id']),
            category='merge-request',
            comments='%s\n\n%s' % (request['title'], request['description']),
            files=self.describe_files(changes['changes']),
            when_timestamp=datetime.now(),
            branch=request['source_branch'],
            project=project,
            repository=source_project_info['http_url_to_repo'],
            src='git',
            properties={
                'source_project_id': request['source_project_id'],
                'source_branch': request['source_branch'],
                'merge_request_id': request['id'],
                'target_project_id': request['target_project_id'],
                'rooturl': 'https://%s' % self.host,
                'try_user_fork': True,
                'owner': source_project_info['owner']['username'],
                'cdash_time': self.safe_now().strftime(cdash.TIMEFORMAT),
                'buildbot_commands': command_list,
            })


class GitlabIntegrationBranchPoller(GitlabPoller):
    compare_attrs = [
        'projects',
    ]

    def __init__(self, host, token, projects=[], **kwargs):
        GitlabPoller.__init__(self, 'GitlabIntegrationBranchPoller(%s)', host, token, **kwargs)

        self.projects = projects

    def describe(self):
        msg = GitlabPoller.describe(self)
        if self.projects:
            items = []
            for project, branches in self.projects.items():
                items.append('%s: %s' % (project, ', '.join(branches)))
            msg += ' (%s)' % '; '.join(items)
        return msg

    @defer.inlineCallbacks
    def poll(self):
        self.last_poll_time = datetime.now()
        for project, branches in self.projects.items():
            pid = urllib.quote(project.lower(), '')
            yield self._poll_project(pid, project, branches)
        yield self.setState('lastRev', self.last_rev)

    @defer.inlineCallbacks
    def _poll_project(self, pid, project, branches):
        project_info = self.api.getproject(pid)

        for branch in branches:
            branch_info = self.api.getbranch(pid, branch)
            if not branch_info:
                log.err('no such branch %s for integration testing on %s' % (branch, project))
                continue

            commit = branch_info['commit']
            sha = commit['id']

            key = unicode('%s.%s' % (pid, branch))
            sha = unicode(sha)

            if self.last_rev.get(key) != sha:
                self.last_rev[key] = sha

                yield self.master.addChange(
                    author='%(author_name)s <%(author_email)s>' % commit,
                    revision=commit['id'],
                    category='integration-branch',
                    comments=commit['message'],
                    # TODO: get the files changed.
                    files=['TODO'],
                    when_timestamp=datetime.now(),
                    branch=branch,
                    project=project,
                    repository=project_info['http_url_to_repo'],
                    src='git',
                    properties={
                        'rooturl': 'https://%s' % self.host,
                        'try_user_fork': False,
                        'cdash_time': self.safe_now().strftime(cdash.TIMEFORMAT),
                    })

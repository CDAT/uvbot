#!/usr/bin/env python

import os
from datetime import datetime
import json

import pymongo
import tangelo
import requests

import dashboard

global _geojs_test_mongo

_cdash_url = 'http://my.cdash.org/index.php?project=geojs'
_geojs_test_mongo = None
_github_api = 'https://api.github.com'
_geojs_owner = 'OpenGeoscience'
_geojs_repo = 'geojs'
_auth_token = os.environ.get('GEOJS_DASHBOARD_KEY')
if not _auth_token:
    try:
        _auth_token = json.loads(
            open(
                os.path.expanduser('~/.geojs_dashboard_config.json'),
                'r'
            ).read()
        )['dashboard_key']
    except Exception:
        pass

if not _auth_token:
    raise Exception('GEOJS_DASHBOARD_KEY required.')


def mongo_client():
    global _geojs_test_mongo
    if _geojs_test_mongo is None or not _geojs_test_mongo.alive():
        _geojs_test_mongo = pymongo.MongoClient()
    return _geojs_test_mongo


def mongo_database():
    return mongo_client()['geojs_dashboard']


def add_push(obj):
    db = mongo_database()

    # get the branch name w/o refs/heads
    branch = '/'.join(obj['ref'].split('/')[2:])

    # get the new commit hash
    commit = obj['after']

    # get the username of the person who pushed the branch
    user = obj['pusher']['name']

    # get the time of the commit
    timestamp = datetime.now()  # fromtimestamp(obj['pushed_at'])

    # check if the hash has already been tested
    tested = db['results']
    if tested.find_one({'hash': commit}):
        return

    # queue the commit for testing
    queue = db['queue']
    result = queue.find_one({'branch': branch})
    if result is None:
        result = {}

    result = {
        'branch': branch,
        'commit': commit,
        'user': user,
        'time': timestamp
    }

    queue.update({'branch': branch}, result, upsert=True)


def handle_status(obj):
    # if it is an error status of any kind then
    # do nothing (let travis handle the non webgl
    # errors)

    if obj['state'] != 'success':
        return

    # check if this is a status message from travis
    target = obj['context']
    if target.find('travis-ci') < 0:
        return

    # TODO: handle multiple branches?
    branch = obj['branches'][0]['name']
    context = branch + '/geojs_dashboard'

    # it is a success message from travis so mark
    # a new status of pending
    url = '/'.join((
        _github_api,
        'repos',
        _geojs_owner,
        _geojs_repo,
        'statuses',
        obj['commit']['sha']
    ))
    data = json.dumps({
        'state': 'pending',
        'target_url': _cdash_url,
        'context': context,
        'description': 'running dashboard tests'
    })
    resp = requests.post(
        url,
        auth=(_auth_token, 'x-oauth-basic'),
        data=data
    )
    if not resp.ok:
        raise Exception("Could not set pending status.")

    # run the dashboard test locally
    try:
        status = dashboard.main(
            obj['commit']['sha'],
            branch,
            obj['commit']['committer']['login']
        )
    except Exception as e:
        # something went wrong in the dashboard, so set the
        # status to error
        data = json.dumps({
            'state': 'error',
            'target_url': _cdash_url,
            'context': context,
            'description': 'Dashboard failure detected: ' + str(e)
        })
        requests.post(
            url,
            auth=(_auth_token, 'x-oauth-basic'),
            data=data
        )
        return

    # set status
    if status['pass']:
        data = json.dumps({
            'state': 'success',
            'target_url': _cdash_url,  # can we get the actual url of the test from cdash?
            'context': context,
            'description': 'All geojs dashboard tests passed!'
        })
        requests.post(
            url,
            auth=(_auth_token, 'x-oauth-basic'),
            data=data
        )
    else:
        data = json.dumps({
            'state': 'failure',
            'target_url': _cdash_url,  # can we get the actual url of the test from cdash?
            'context': context,
            'description': 'One or more dashboard tests failed.'
        })
        requests.post(
            url,
            auth=(_auth_token, 'x-oauth-basic'),
            data=data
        )


@tangelo.restful
def get(*arg, **kwarg):
    return 'I hear you!'


@tangelo.restful
def post(*arg, **kwarg):

    headers = tangelo.request_headers()

    if headers.get('X-Github-Event') not in ('status', 'push'):
        return tangelo.HTTPStatusCode(400, "Unhandled event")

    body = tangelo.request_body()
    s = body.read()

    try:
        obj = json.loads(s)
    except:
        return tangelo.HTTPStatusCode(400, "Could not load json object.")

    if headers['X-Github-Event'] == 'status':
        handle_status(obj)
    elif headers['X-Github-Event'] == 'push':
        add_push(obj)

    return 'OK'

import json, threading, queue
from datetime import datetime
import requests
from requests.api import request
from requests.auth import HTTPBasicAuth
from settings import Settings

safetyLock = threading.Lock()

class JenkinsRequestWorker(threading.Thread):
    def __init__(self, project_name, auth_credentials, request_queue, retval):
        super(JenkinsRequestWorker, self).__init__(daemon=True)
        self.project_name = project_name
        self.request_queue = request_queue
        self.auth_credentials = auth_credentials
        self.retval = retval

    def run(self):
        while True:
            env = self.request_queue.get()

            request_url = f"{env['url']}api/json"

            response = requests.get(request_url, auth=self.auth_credentials, verify=False)
            if response.status_code >= 400:
                raise Exception("Error retrieving jobs.")

            parsed_response = response.json()

            for job in parsed_response['jobs']:
                if self.project_name.lower() in job['name'].lower() and 'prod' in job['name'].lower():
                    safetyLock.acquire()
                    self.retval[env['name']]['jobs'].append({
                        'name': job['name'],
                        'url': job['url'],
                        'type': 'PROD'
                    })
                    safetyLock.release()
                elif self.project_name.lower() in job['name'].lower() and 'qa' in job['name'].lower():
                    safetyLock.acquire()
                    self.retval[env['name']]['jobs'].append({
                        'name': job['name'],
                        'url': job['url'],
                        'type': 'QA'
                    })
                    safetyLock.release()

            self.request_queue.task_done()


class JenkinsBuild(object):
    def __init__(self, data):
        self.name = data['fullDisplayName']
        self.id = data['id']
        self.date = datetime.fromtimestamp(data['timestamp'] / 1000)
        self.hash = ''
        self.tag = ''

        self.parse_actions(data)

    def parse_actions(self, data):
        for action in data['actions']:
            if '_class' in action and action['_class'] == 'hudson.plugins.git.util.BuildData':
                if 'lastBuiltRevision' in action:
                    self.hash = action['lastBuiltRevision']['SHA1']

                    if 'branch' in action['lastBuiltRevision']:
                        self.tag = action['lastBuiltRevision']['branch'][0]['name']

class JenkinsAPI:
    def __init__(self, base_url=None, username=None, token=None):
        if base_url is None:
            self.base_url = Settings.get_setting('jenkins_base_url')
        else:
            self.base_url = base_url

        if username is None:
            self.username = Settings.get_setting('jenkins_username')
        else:
            self.username = username

        if token is None:
            self.token = Settings.get_setting('jenkins_api_token')
        else:
            self.token = token

        if (self.base_url is None or
            self.username is None or
            self.token is None):
            raise Exception("A base_url, username and API token \
                are required to use the JenkinsAPI.")

        self.auth_credentials = HTTPBasicAuth(self.username, self.token)

        if not self.test_connection():
            raise Exception("Failed to connect to jenkins.")

    @property
    def base_url_slashed(self):
        if self.base_url.endswith('/'):
            return self.base_url
        else:
            return f"{self.base_url}/"

    def test_connection(self) -> bool:
        request_url = f"{self.base_url_slashed}api/json/"

        try:
            response = requests.get(request_url, auth=self.auth_credentials, verify=False)
            if response.status_code != 200:
                return False
            return True
        except Exception as e:
            return False

    def get_environments(self):
        request_url = f"{self.base_url_slashed}/api/json"

        response = requests.get(request_url, auth=self.auth_credentials, verify=False)
        if response.status_code >= 400:
            raise Exception("Failed to connect or invalid endpoint.")

        parsed_response = response.json()

        retval = []

        for job in parsed_response['jobs']:
            retval.append({
                'name': job['name']
            })

        return retval


    def get_jobs(self, project_name):
        envs = Settings.get_setting('envs')

        if envs is None:
            return None

        retval = {}

        for env in envs:
            retval[env['name']] = {
                'jobs': []
            }

        request_queue = queue.Queue()

        for x in range(5):
            JenkinsRequestWorker(project_name, self.auth_credentials, request_queue, retval).start()

        for env in envs:
            request_queue.put(env)

        request_queue.join()

        return retval


    def get_job_details(self, job_url):
        request_url = f"{job_url}/api/json"

        response = requests.get(request_url, auth=self.auth_credentials, verify=False)
        if response.status_code >= 400:
            raise Exception("Error retrieving job details")

        parsed_response = response.json()

        return parsed_response

    def get_build_details(self, build_url):
        request_url = f"{build_url}/api/json"

        response = requests.get(request_url, auth=self.auth_credentials, verify=False)
        if response.status_code >= 400:
            raise Exception("Error retrieving job details")

        parsed_response = response.json()

        retval = JenkinsBuild(parsed_response)

        return retval

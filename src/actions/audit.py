from api.jenkins import JenkinsAPI
from PyInquirer import prompt
from pushutil.settings import Settings

from halo import Halo
from tabulate import tabulate

class Auditor:
    def __init__(self, env, audit_env, audit_output=None):
        self.env = env
        self.audit_env = audit_env
        self.audit_output = audit_output
        self.jenkins = None

    def configure(self):
        if not self.jenkins:
            self.jenkins = JenkinsAPI()

    def execute(self):
        spinner = Halo(text='Gathering jobs...', spinner='dots', color='cyan')
        spinner.start()
        self.configure()
        self.results = []

        envs = self.jenkins.get_environments()

        env_question = [
            {
                'type': 'checkbox',
                'name': 'envs',
                'message': 'Choose the directories to audit:',
                'choices': envs
            }
        ]

        env_answers = prompt(env_question)

        env_names = []

        for ans in env_answers['envs']:
            env_names.append({
                'name': ans,
                'url': f"{self.jenkins.base_url_slashed}job/{ans}"
            })

        for env in env_names:
            all_jobs = self.jenkins.get_all_jobs(env)
            found_main_list = [x for x in all_jobs if self.audit_env.lower() in x['name'].lower()]

            for f in found_main_list:
                self.results.append({
                    'env': env,
                    'audit_job_name': f['name'],
                    'audit_job_url': f['url'],
                    'found_job_name': None,
                    'found_job_url': None
                })

            for result in self.results:
                job_name = result['audit_job_name']
                name_lower = job_name.lower().replace(self.audit_env.lower(), self.env.lower()).lower()
                found = next(filter(lambda x: x['name'].lower() == name_lower, all_jobs), None)

                if found:
                    result['found_job_name'] = found['name']
                    result['found_job_url'] = found['url']

        spinner.stop()

        if self.audit_output:
            self.write_output()
        else:
            self.print_output()


    def print_output(self):
        print(f"A {self.env} job could not be found for the following:")

        for result in self.results:
            if result['found_job_name'] is None:
                print(f"""
{self.env} Job Name: {result['audit_job_name']}
{self.env} Job URL : {result['audit_job_url']}
Environment: {result['env']['name']}

                """)


    def write_output(self):
        with open(self.audit_output, 'w') as f:
            f.write(f"A {self.env} job could not be found for the following:")

            for result in self.results:
                if result['found_job_name'] is None:
                    f.write(f"""
{self.env} Job Name: {result['audit_job_name']}
{self.env} Job URL : {result['audit_job_url']}
Environment: {result['env']['name']}
                    """)



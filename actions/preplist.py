from api.jenkins import JenkinsAPI
from api.deployment import DeploymentTask
import io
from PyInquirer import prompt
from settings import Settings

from halo import Halo
class PushListParser:
    def __init__(self, args):
        self.repo = args.repo
        self.version = args.version
        self.prev_version = args.previous_version
        self.tw_task = args.tw_task
        self.jenkins = None


    @property
    def release_notes_url(self):
        return f"{self.repo.url}releases/tag/{self.version}"

    @property
    def current_production_hash(self):
        return '';

    def configure(self):
        if not self.jenkins:
            self.jenkins = JenkinsAPI()

    def get_diff_url(self, previous_hash):
        if previous_hash == 'N/A':
            return 'N/A'

        return f"{self.repo.url}compare/{previous_hash}...{self.version}"


    def execute(self):
        spinner = Halo(text='Gathering jobs...', spinner='dots', color='cyan')
        spinner.start()
        self.configure()

        jobs = self.jenkins.get_jobs(self.repo.name)

        retval = ""

        for env_name, env in jobs.items():
            try:
                prod_job = next(obj for obj in env['jobs'] if 'prod' in obj['name'].lower())
            except StopIteration:
                prod_job = None

            try:
                qa_job   = next(obj for obj in env['jobs'] if 'qa' in obj['name'].lower())
            except StopIteration:
                qa_job = None

            if not prod_job or not qa_job:
                continue

            task = DeploymentTask(self.repo, prod_job, qa_job, self.jenkins, self.version)

            retval += f"""
Task    : Deploy {self.repo.name} {self.version} to PROD
TW Task : {self.tw_task}
Release : {self.release_notes_url}
Diff    : {self.get_diff_url(task.prod_hash)}
ENV     : {env_name}
QA Hash : {task.qa_hash}
Deploy  : {self.repo.get_tag_hash(self.version)}
PROD    : {task.prod_details}
JOB URL : {task.prod_job['url']}


                """

        spinner.stop()

        print(retval)


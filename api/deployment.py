

class DeploymentTask:
    def __init__(self, repo, prod_job, qa_job, jenkins_con, version):
        self.repo = repo
        self.prod_job = prod_job
        self.qa_job = qa_job
        self.jenkins = jenkins_con
        self.version = version

        self.deployment_hash = self.repo.get_tag_hash(self.version)

        if self.prod_job is not None and 'url' in prod_job.keys():
            self.prod_job_details = self.jenkins.get_job_details(self.prod_job['url'])

        if self.qa_job is not None and 'url' in qa_job.keys():
            self.qa_job_details = self.jenkins.get_job_details(self.qa_job['url'])

        if self.prod_job_details is not None and 'lastCompletedBuild' in self.prod_job_details:
                self.last_build_prod = self.jenkins.get_build_details(self.prod_job_details['lastCompletedBuild']['url']) \
                    if self.prod_job_details['lastCompletedBuild'] is not None \
                    else None

        if self.qa_job_details is not None and 'lastCompletedBuild' in self.qa_job_details:
                self.last_build_qa = self.jenkins.get_build_details(self.qa_job_details['lastCompletedBuild']['url']) \
                    if self.qa_job_details['lastCompletedBuild'] is not None \
                    else None


    @property
    def qa_matches(self):
        if self.last_build_qa is not None:
            return self.last_build_qa.hash == self.deployment_hash

        return False

    @property
    def qa_hash(self):
        return self.last_build_qa.hash \
            if self.last_build_qa is not None \
            else 'N/A'

    @property
    def prod_details(self):
        retval = ''
        if self.last_build_prod is not None:
            retval += self.last_build_prod.hash

        if tag := self.repo.get_hash_tag(self.last_build_prod.hash):
            retval += f" ({tag})"

        if self.last_build_prod is not None:
            retval += f" {self.last_build_prod.date.strftime('%m/%d/%Y')}"

        return retval if retval != '' else 'N/A'

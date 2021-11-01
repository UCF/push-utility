import os
import re
from github import Github
from pushutil.settings import Settings

class GHRepo:
    def __init__(self, project):
        http_re = re.compile(r'(?!http|https)\:\/\/github\.com\/(?P<user>[\w_-]+)\/(?P<repo>[\w_-]+)')
        ssh_re = re.compile(r'git@github\.com\:(?P<user>\w+)\/(?P<repo>[\w_-]+)')

        if project.startswith('http'):
            # It's an http(s) path
            match = http_re.search(project)
            groups = match.groupdict()
            self.user = groups['user']
            self.project_name = groups['repo']
        elif project.startswith('git@'):
            # It's an ssh path
            match = ssh_re.search(project)
            groups = match.groupdict()
            self.user = groups['user']
            self.project_name = groups['repo']
        elif os.path.exists(project):
            # It's a file path
            self.user = Settings.get_setting('github_user')
            self.project_name = os.path.basename(project)
        else:
            # It's probably just the project name
            self.user = Settings.get_setting('github_user')
            self.project_name = project

        self.access_token = Settings.get_setting('github_token')

        if self.access_token is None:
            raise Exception('A github token is required')

        self.tags = []

        self.resolve_repo()

    @property
    def tags_as_options(self):
        retval = []
        for tag in self.tags:
            retval.append(tag.name)

        return retval

    def resolve_repo(self):
        gh = Github(self.access_token)
        self.repo = gh.get_repo(f"{self.user}/{self.project_name}")

        for tag in self.repo.get_tags():
            self.tags.append(tag)

    def get_tag_hash(self, tag):
        for t in self.tags[0:5]:
            if t.name == tag:
                return t.commit.sha

        return None

    def get_hash_tag(self, hash):
        for t in self.tags:
            if t.commit.sha == hash:
                return t.name

        return None

    @property
    def name(self):
        return self.repo.name

    @property
    def url(self):
        return f"{self.repo.html_url}/"


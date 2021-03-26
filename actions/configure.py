from api.jenkins import JenkinsAPI
import io
from settings import Settings
from PyInquirer import prompt

class ConfigureUtility:
    def __init__(self):
        self.initial_questions = [
            {
                "type": "input",
                "name": "jenkins_base_url",
                "message": "Jenkins Base URL:"
            },
            {
                "type": "input",
                "name": "jenkins_username",
                "message": "Jenkins User Name:"
            },
            {
                "type": "password",
                "name": "jenkins_api_token",
                "message": "Jenkins API Token:"
            }
        ]

    def get_environments(self, jenkins):
        envs = jenkins.get_environments()

        return envs

    def execute(self):
        settings_dict = prompt(self.initial_questions)

        jenkins = JenkinsAPI(
            settings_dict['jenkins_base_url'],
            settings_dict['jenkins_username'],
            settings_dict['jenkins_api_token']
        )

        if not jenkins.test_connection():
            raise Exception("Unable to connect to jenkins with those settings.")

        envs = self.get_environments(jenkins)

        env_question = [
            {
                'type': 'checkbox',
                'name': 'envs',
                'message': 'Choose the environments you deploy to:',
                'choices': envs
            }
        ]

        env_answers = prompt(env_question)

        env_names = []

        for ans in env_answers['envs']:
            env_names.append({
                'name': ans,
                'url': f"{jenkins.base_url_slashed}job/{ans}/"
            })

        settings_dict.update({
            'envs': env_names
        })

        github_questions = [
            {
                'type': 'input',
                'name': 'github_user',
                'message': 'What is your default Github User or Org:'
            },
            {
                'type': 'input',
                'name': 'github_token',
                'message': 'What is your Github access token.'
            }
        ]

        github_answers = prompt(github_questions)

        settings_dict.update(github_answers)

        Settings.write_settings(settings_dict)


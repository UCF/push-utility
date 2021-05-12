import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import argparse
from PyInquirer import prompt
import json
import io

from actions.configure import ConfigureUtility
from actions.preplist import PushListParser
from api.github_repo import GHRepo

parser = argparse.ArgumentParser()

parser.add_argument(
    'repo',
    type=str,
    help='The repository to deploy.',
    nargs="?"
)

parser.add_argument(
    'version',
    type=str,
    help="The version or hash being pushed.",
    nargs="?"
)

parser.add_argument(
    'previous_version',
    type=str,
    help="The previous version that was pushed.",
    nargs="?"
)

parser.add_argument(
    'tw_task',
    type=str,
    help='The teamwork job for the push',
    nargs="?"
)

parser.add_argument(
    '--configure',
    action='store_true',
    dest='configure',
    help="Triggers a configuration routine"
)

def process_args(args):
    if args.repo:
        args.repo = GHRepo(args.repo)

    if not args.version:
        questions = [
            {
                'type': 'list',
                'name': 'tag',
                'message': 'Which tag do you want to deploy:',
                'choices': args.repo.tags_as_options
            },
        ]

        ans = prompt(questions)
        args.version = ans['tag']

    return args

def main():
    args = parser.parse_args()

    if args.configure:
        command = ConfigureUtility()
    else:
        args = process_args(args)
        command = PushListParser(args)
        command.configure()

    try:
        command.execute()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

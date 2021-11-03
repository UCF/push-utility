# Push Utility

This is a simple python utility that gathers information about a repository, and recent push information about that repository into a compact message that we use to verify what we're pushing and what the state of production is prior to pushing.

## Setup
1. Install the utility. The utility requires python3, so you may have to install using `pip3`: `pip3 install git+https://github.com/UCF/push-utility.git`.
2.

## Setup for Contributing
1. Create a python3 venv where the project will reside: `python3 -m venv push-utility`
2. Clone this repository into a `src` directory of that venv: `cd push-utility && git clone https://github.com/UCF/push-utility/.git src`.
3. Activate the virtual environment: `source ../bin/activate`.
4. Install the required python packages: `pip install -r requirements.txt`.

## Configuration
This utility requires you to have access to Jenkins and GitHub via their APIs. In both cases, API Tokens are used to authenticate. Below are links describing how to generate an API token for each:

[Jenkins API Token](https://stackoverflow.com/questions/45466090/how-to-get-the-api-token-for-jenkins#answer-45466184)

[GitHub API Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

Once these tokens have been created an securely stored, you can run the configuration process of the utility:

`python app.py --configure`

The first series of questions will prompt you for the following:

1. The root URL of Jenkins
2. Your Jenkins username
3. Your Jenkins token

Your credentials will be immediately tested against the API. If there is a problem with the credentials, and error will be thrown and the configuration process will exit out. If successful, a list of our Jenkins "directories" will be listed. Choose all the directories which contains jobs you are responsible for pushing.

Once you have chosen your Jenkins directories, you will be prompted for the following information:

1. Your GitHub username or Org name
2. Your access token

Note, the username provided also determines where the utility will look for repositories when pulling information. If using this within an organizational setting, be sure to use the name of your Org here, and not your username.

## Usage
There are two basic ways to run the utility:

### Verbosely

You are able to specify all the input data yourself within the command line arguments when you run the utility. The options are as follows:

```
usage: app.py [-h] [--configure] [repo] [version] [previous_version] [tw_task]

positional arguments:
  repo              The repository to deploy.
  version           The version or hash being pushed.
  previous_version  The previous version that was pushed.
  tw_task           The teamwork job for the push

```

2. Wizardly

Alternatively, you can also provide only the repository name and use a simple wizard to choose the other options:

```
> python app.py Athena-Framework

? Which tag do you want to deploy: (Use arrow keys)
> v1.1.0
  v1.0.8
  v1.0.7
  ...

```

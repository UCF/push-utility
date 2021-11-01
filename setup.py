from setuptools import setup, find_packages

with open('readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='push-utility-ucf',
    version='1.0.0',
    author='UCF Web Communications',
    author_email='webcom@ucf.edu',
    description='Utility for gathering information on deployments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/UCF/push-utility/',
    python_requires='>=3.0.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'pushutil=pushutil.app:main'
        ]
    },
    install_requires=[
        'halo==0.0.31',
        'PyGithub==1.54.1',
        'PyInquirer==1.0.3',
        'PyJWT==1.7.1',
        'requests==2.25.1',
        'tabulate==0.8.9',
        'tqdm==4.60.0',
        'urllib3==1.26.3'
    ]
)

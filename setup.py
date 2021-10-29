from setuptools import setup

setup(
    name='ucf-push-utility',
    version='1.0.0',
    python_requires='>3.0.0',
    entry_points={
        'console_scripts': [
            'pushutil=app:main'
        ]
    },
    install_requires=[
        'PyGithub==1.54.1',
        'PyInquirer==1.0.3',
        'PyJWT==1.7.1',
        'requests==2.25.1',
        'tqdm==4.60.0',
        'urllib3==1.26.3'
    ]
)

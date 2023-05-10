from setuptools import setup, find_packages

setup(
    name='ethup',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
        'GitPython',
    ],
    entry_points={
        'console_scripts': [
            'ethup = ethup:main',
        ],
    },
)

from setuptools import setup
from setuptools import find_packages

setup(
    name='SPLcli',
    version='0.1.0',
    py_modules=['SPLcli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'SPLcli = SPLcli:main',
        ]},
    packages=find_packages(
        where='./src',
        include=['SPLcli*'],
        exclude=['SPLcli.tests'],),
)

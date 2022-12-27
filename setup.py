from setuptools import setup

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
        ],
    },
)

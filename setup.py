from setuptools import setup

setup(
    name='logParser',
    version='0.1.0',
    py_modules=['cliInterface'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cliInterface = src.cliInterface:main',
        ],
    },
)
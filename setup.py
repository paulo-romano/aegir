from setuptools import setup

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name="Aegir",
    version='0.0.1',
    py_modules=['aegir'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        aegir=aegir:aegir_commands
    ''',
)

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='phonebooth api',
    version='0.0.1',
    description='Simple but effective REST API for PhoneBooth notification system.',
    long_description=readme,
    author='Carlos Perez',
    author_email='carlos@searchkings.ca',
    url='https://git.heroku.com/phonebooth-api.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


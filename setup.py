#!/usr/bin/env python

from setuptools import setup

setup(
    name='logstats',
    version='0.1',
    description='A module to collect and display stats for long running processes',
    author='Alberto Granzotto',
    author_email='agranzot@gmail.com',
    packages=['logstats'],
    test_suite='logstats.test'
)

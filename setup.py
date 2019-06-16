#!/usr/bin/env python3

from setuptools import setup


setup(
     name='ennead',
     version='0.0',
     description='Task management & solutions check system',
     author='Slon School team',
     author_email='schoolslon@gmail.com',
     python_requires='>=3.6.0',
     packages=['ennead'],
     install_requires=open('requirements.txt').read().splitlines()
)

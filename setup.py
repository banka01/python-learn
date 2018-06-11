import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='python-learn',
    version='1.0',
    packages=['sample'],
    url='',
    license='',
    author='bankar',
    author_email='bankar',
    description='demo project',
    long_description=read('README.md')

)

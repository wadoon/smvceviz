#!/usr/bin/python3

from distutils.core import setup

setup(
    name='smvceviz',
    version='0.1',
    packages=[''],
    py_modules = ['smvcce'],
    url='http://github.com/areku/smvceviz',
    license='gpl-v3',
    author='Alexander Weigl',
    author_email='Alexander.Weigl@student.kit.edu',
    description='Visualize the Traces of NuSMV and NuXMV',
    requires=['Jinja2']
)

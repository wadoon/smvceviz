#!/usr/bin/python3
from setuptools import setup

setup(
    name='smvceviz',
    version='0.1',
    packages= ['smvceviz'],
    url='http://github.com/areku/smvceviz',
    include_package_data = True,
    license='gpl-v3',
    author='Alexander Weigl',
    author_email='Alexander.Weigl@student.kit.edu',
    description='Visualize the Traces of NuSMV and NuXMV',
    requires=['Jinja2'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    entry_points = {
        "console_scripts": [
            'smvceviz = simceviz:main'
        ]
    },
)

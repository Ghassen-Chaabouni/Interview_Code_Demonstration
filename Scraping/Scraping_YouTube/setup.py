#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import find_packages, setup


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version
	
__version__ = find_version('youtube_driver/__init__.py')

files = ["config/*"]

setup(
	name='youtube-driver',
	version=__version__,
	description='Scraping Youtube comments',
	long_description=read('README.md'),
	url='#',
	author='Ghassen Chaabouni',
	author_email='ghassen1302@live.com',
	license='MIT',
	packages=['youtube_driver'],
	zip_safe=False,
	package_data = {'youtube_driver' : files },
	install_requires=parse_requirements('requirements.txt'),
	entry_points={
        'console_scripts': [
            'youtube-driver=youtube_driver.__main__:main',
        ]
    }
)


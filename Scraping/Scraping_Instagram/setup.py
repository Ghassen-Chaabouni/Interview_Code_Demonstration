import os
import io
import sys
import setuptools

from setuptools import setup

version = "1.0.0"

with io.open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt')

# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir) for ir in install_reqs if not str(ir).startswith("-") ]

setup(
    name='insta_crawler',
    version=version,
    description=('Scraping Instagram profils'),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jawher Bouhouch',
    author_email='jbouhouch@geeksdata.fr',
    packages=[
        'insta_crawler',
    ],
    # packages= setuptools.find_packages(),
    package_dir={'insta_crawler': 'insta_crawler'},
    include_package_data=True,
    install_requires=reqs,
    license='MIT',
    entry_points={
        'console_scripts': [
            'insta=insta_crawler.__main__:main',
        ]
    }
)
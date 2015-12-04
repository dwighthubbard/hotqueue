#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from setuptools import setup


METADATA_FILENAME = 'hotqueue/package_metadata.json'
BASEPATH = os.path.dirname(os.path.abspath(__file__))


def readme():
    for filename in ['README.rst', 'README.txt']:
        if os.path.exists(filename):
            with open(filename) as f:
                return f.read()
    return ''


def scripts():
    """
    Return the list of scripts in the scripts directory
    :return:
    """
    if os.path.isdir('scripts'):
        return [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]


class Git(object):
    version_list = ['0', '7', '0']

    def __init__(self, version=None):
        if version:
            self.version_list = version.split('.')

    @property
    def version(self):
        """
        Generate a Unique version value from the git information
        :return:
        """
        git_rev = len(os.popen('git rev-list HEAD').readlines())
        if git_rev != 0:
            self.version_list[-1] = '%d' % git_rev
        version = '.'.join(self.version_list)
        return version

    @property
    def branch(self):
        """
        Get the current git branch
        :return:
        """
        return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    @property
    def hash(self):
        """
        Return the git hash for the current build
        :return:
        """
        return os.popen('git rev-parse HEAD').read().strip()

    @property
    def origin(self):
        """
        Return the fetch url for the git origin
        :return:
        """
        for item in os.popen('git remote -v'):
            split_item = item.strip().split()
            if split_item[0] == 'origin' and split_item[-1] == '(push)':
                return split_item[1]


def get_and_update_metadata():
    """
    Get the package metadata or generate it if missing
    :return:
    """
    global METADATA_FILENAME

    if not os.path.exists('.git') and os.path.exists(METADATA_FILENAME):
        with open(METADATA_FILENAME) as fh:
            metadata = json.load(fh)
    else:
        git = Git(version=setup_arguments['version'])
        metadata = {
            'git_version': git.version,
            'git_origin': git.origin,
            'git_branch': git.branch,
            'git_hash': git.hash,
            'version': git.version,
        }
        with open(METADATA_FILENAME, 'w') as fh:
            json.dump(metadata, fh, indent=4)
    return metadata


setup_arguments = dict(
    author="Dwight Hubbard",
    author_email="d@d-h.us",
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description="A fork of the HotQueue Python library that allows you to use "
                "Redis/Redislite as a message queue.",
    include_package_data=True,
    install_requires=[
        'redis>=2.0.0',
        'redislite>-1.0.254'
    ],
    license="MIT",
    long_description=readme(),
    name="redislite-hotqueue",
    packages=['hotqueue'],
    package_data={
        'hotqueue': ['package_metadata.json'],
    },
    py_modules=['hotqueue'],
    scripts=scripts(),
    url="http://github.com/dwighthubbard/hotqueue",
    version='1.3.0',
)


if __name__ == '__main__':
    metadata = get_and_update_metadata()
    setup_arguments['version'] = metadata['version']

    setup(**setup_arguments)

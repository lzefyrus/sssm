#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sssm_jpmorgan

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

package_data = {
}

requires = [
]

classifiers = [
    'Development Status :: 0.1 - Beta',
    'Intended Audience :: JPMorgan',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='sssm-jpmorgan',
    version=sssm_jpmorgan.__version__,
    description='Super Simple Stock Market',
    long_description=readme,
    data_files=[('csv', ['sssm_jpmorgan/data/sample.csv'])],
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    install_requires=requires,
    author=sssm_jpmorgan.__author__,
    author_email='python@chrisstreeter.com',
    url='https://github.com/lzefyrus/sssm-jpmorgan',
    license='MIT',
    classifiers=classifiers,

)

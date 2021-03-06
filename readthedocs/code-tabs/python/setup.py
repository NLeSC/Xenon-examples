#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit pyxenon_snippets/__version__.py
version = {}
with open(os.path.join(here, 'pyxenon_snippets', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='pyxenon_snippets',
    version=version['__version__'],
    description="code snippets for pyxenon tutorial",
    long_description=readme + '\n\n',
    author="Jurriaan H. Spaaks",
    author_email='j.spaaks@esciencecenter.nl',
    url='https://github.com/xenon-middleware/xenon-tutorial',
    packages=[
        'pyxenon_snippets',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='pyxenon_snippets',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=[],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ]
)

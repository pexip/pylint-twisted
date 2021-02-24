# -*- coding: utf-8 -*-
from distutils.core import setup
import sys


_version = '0.2'
_packages = ['pylint_twisted']

_short_description = "pylint-twisted is a Pylint plugin to aid Pylint in \
recognizing and understanding errors caused when using Twisted"

_install_requires = [
    'pylint-plugin-utils>=0.2.1'
]


_install_requires += [
    'pylint>=1.0',
    'astroid>=1.0',
]

setup(
    name='pylint-twisted',
    url='https://github.com/pexip/pylint-twisted',
    author='Pexip AS',
    author_email='packaing@pexip.com',
    description=_short_description,
    version=_version,
    packages=_packages,
    install_requires=_install_requires,
    license='GPLv2',
    download_url=("https://github.com/pexip/pylint-twisted/tarball/v" +
                  str(_version)),
    keywords='pylint twisted plugin'
)

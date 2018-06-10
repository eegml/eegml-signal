# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import setuptools # required to allow for use of python setup.py develop, may also be important for cython/compiling if it is used

from distutils.core import setup


setup(
    name = 'eegml-signal',
    version='0.0.1',
    description="""signal processing for eeg""",
    author="""Chris Lee-Messer""",
    url="https://gitlab.lee-messer.net/cleemesser/eegml-signal",
    # download_url="",
    classifiers=['Topic :: Science :: EEG'],
    packages=['eegml_signal'],
    # package_data={}
    # data_files=[],
    # scripts = [],
    )

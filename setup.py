# Copyright (C) 2017-2019 COAL Developers
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth 
# Floor, Boston, MA 02110-1301, USA.

import os.path
from setuptools import find_packages, setup

# Package data
# ------------
_author = 'COAL Developers'
_author_email = 'coal-capstone@googlegroups.com'
_classifiers = ['Environment :: Console', 'Intended Audience :: Developers',
                'Intended Audience :: Information Technology',
                'Intended Audience :: Science/Research',
                'Topic :: Scientific/Engineering',
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: GNU General Public License v2 ('
                'GPLv2)',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python '
                'Modules', ]
_description = 'COAL mining library for AVIRIS data.'
_download_url = 'http://pypi.python.org/pypi/pycoal/'
_requirements = ["numpy", "spectral", "guzzle_sphinx_theme", "joblib", "psutil", 
                 "wxpython", "pyopengl", "torch", "tqdm"]
_keywords = ['spectroscopy', 'aviris', 'aviris-ng', 'mining', 'minerals']
_license = 'GNU GENERAL PUBLIC LICENSE, Version 2'
_long_description = 'A python suite for the identification and ' \
                    'characterization of mining activity within AVIRIS data.'
_name = 'pycoal'
_namespaces = []
_test_suite = 'pycoal.tests'
_url = 'https://github.com/capstone-coal/pycoal'
_version = '0.5.2'
_zip_safe = False
_entry_points = {
    'console_scripts': ['pycoal-mineral = pycoal.cli.mineral:main',
                        'pycoal-mining = pycoal.cli.mining:main',
                        'pycoal-environment = pycoal.cli.environment:main']}


# Setup Metadata
# --------------


def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = '\n\n'.join([_header, _read('README.rst')])
open('doc.txt', 'w').write(_longDescription)

setup(author=_author, author_email=_author_email, classifiers=_classifiers,
      description=_description, download_url=_download_url,
      include_package_data=True, install_requires=_requirements,
      keywords=_keywords, license=_license, long_description=_long_description,
      name=_name, namespace_packages=_namespaces, packages=find_packages(
        exclude=["examples", "pycoal/tests"]),
      test_suite=_test_suite, url=_url, version=_version, zip_safe=_zip_safe,
      entry_points=_entry_points)

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

import os


# utility function to remove multiple test files
def remove_files(list_of_file_names):
    for file_name in list_of_file_names:
        try:
            os.remove(file_name)
        except OSError:
            pass


# file names of USGS Digital Spectral Library 06 in ENVI format
libraryFilenames = ["s06av95a_envi.hdr", "s06av95a_envi.sli"]


# set up test module before running tests
def setup_module():
    # enter test directory
    os.chdir('pycoal/tests')


# tear down test module after running tests
def teardown_module():
    # leave test directory
    os.chdir('../..')

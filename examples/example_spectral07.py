#!/usr/bin/python
#Copyright (C) 2017-2019 COAL Developers
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
# encoding: utf-8

'''
example_spectral07.py -- a script which will generate envi .sli and .hdr convolved library
files of `USGS Spectral Library Version 7 <https://speclab.cr.usgs.gov/spectral-lib.html>`_

Dependencies
`USGS Spectral Library Version 7 <https://speclab.cr.usgs.gov/spectral-lib.html>`_
must be downloaded and unzipped to the examples directory

All files generated will be located in the examples directory


@author:     COAL Developers

@copyright:  2017-2019 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import os
import sys
import pycoal
sys.path.insert(0, '../pycoal')
import mineral

usgs_convolved = mineral.FullSpectralLibrary7Convert()
usgs_convolved.convert('usgs_splib07')

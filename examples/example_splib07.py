#Copyright (C) 2017-2018 COAL Developers
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
example_splib07.py -- an example script that will generate envi .sli and .hdr files for
a spectral library in ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> format

@author:     COAL Developers

@copyright:  2017-2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import sys
import os
import inspect
import pycoal
sys.path.insert(0, '../pycoal')
reload(sys)
sys.setdefaultencoding('utf8')
import mineral
import math
import numpy
import spectral

#This will generate three files s07av95a_envi.hdr, s07av95a_envi.hdr.sli,splib.db and dataSplib07.db
#For a library in ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> format
library_filename = 'usgs_splib07_modified'
data_dir = "dataSplib07.db"
header_name = "s07av95a_envi"

# create a new mineral aster conversion instance
spectral_envi = mineral.AsterConversion()
# Generate .sli and .hdr
spectral_envi.convert(library_filename,data_dir,header_name)



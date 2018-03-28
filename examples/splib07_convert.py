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
splib07_convert -- a script which will loop through 
This code loops through the USGS Spectral Library version 7
<https://speclab.cr.usgs.gov/spectral-lib.html> and converts all .txt files into
an ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> .spectrum.txt file
ASTER Library Version 2.0 Spectral Library files are in .spectrum.txt file format

@author:     COAL Developers

@copyright:  2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import sys
import os
import pycoal
sys.path.insert(0, '../pycoal')
reload(sys)
sys.setdefaultencoding('utf8')
import mineral
import math
import numpy
import spectral

#This will take the .txt files for Spectra in USGS Spectral Version 7 and
#convert their format to match that of ASTER .spectrum.txt files for spectra
library_filename = 'usgs_splib07_modified/'
# create a new mineral aster conversion instance
spectral_aster = mineral.SpectralToAsterConversion()
# Convert all files
files = os.listdir(library_filename)
for x in range(0, len(files)):
    name = 'usgs_splib07_modified/' + files[x]
    spectral_aster.convert(name)



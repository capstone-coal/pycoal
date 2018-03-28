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
splib07_convolved -- a script which will generate envi .sli and .hdr convolved library
files of USGS Spectral Library Version 7 <https://speclab.cr.usgs.gov/spectral-lib.html>

Dependencies
USGS Spectral Library Version 7 <https://speclab.cr.usgs.gov/spectral-lib.html>
must be downloaded to the examples directory

This code has three parts.
First, it loops through the USGS Spectral Library version 7
<https://speclab.cr.usgs.gov/spectral-lib.html> and moves all spectra files to a
modified directory.
Second, it converts all USGS Spectral Library Version 7 .txt files into
the ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> .spectrum.txt file format using
the SpectralToAsterConversion class in pycoal mineral.
Third, it creates a .db, .sli and .hdr envi files for the convolved spectral library using
the AsterConversion class in pycoal mineral.

All files generated will be located in the examples directory


@author:     COAL Developers

@copyright:  2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

#!/usr/bin/python

import os
import sys
from sys import path
sys.path.insert(0, '../pycoal')
reload(sys)
sys.setdefaultencoding('utf8')
import fnmatch
import shutil
import mineral
import math
import numpy
import spectral

#This will take all the necessary .txt files for spectra in USGS
#Spectral Library Version 7 and put them in a new directory called
#"usgs_splib07_modified" in the examples directory
directory = 'usgs_splib07_modified'
if not os.path.exists(directory):
    os.makedirs(directory)

exclude = set(['usgs_splib07_modified'])
for root, dir, files in os.walk("."):
    dir[:] = [d for d in dir if d not in exclude]
    for items in fnmatch.filter(files, "*.txt"):
        if "Bandpass" not in items:
            if "errorbars" not in items:
                if "Wave" not in items:
                    if "SpectraValues" not in items:
                        shutil.copy2(os.path.join(root,items), directory)

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

#This will generate three files s07av95a_envi.hdr, s07av95a_envi.hdr.sli,splib.db and dataSplib07.db
#For a library in ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> format
library_filename = 'usgs_splib07_modified'
data_dir = "dataSplib07.db"
header_name = "s07av95a_envi"

# create a new mineral aster conversion instance
spectral_envi = mineral.AsterConversion()
# Generate .sli and .hdr
spectral_envi.convert(library_filename,data_dir,header_name)



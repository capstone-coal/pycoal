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
example_ecostress.py -- a script which will generate envi .sli and .hdr convolved library
files of `ECOStress Spectral Library <https://speclib.jpl.nasa.gov/>`_

Dependencies
`ECOStress Spectral Library <https://speclib.jpl.nasa.gov/download>`_
ALL Spectra option must be downloaded to the examples directory.

All files generated will be located in the examples directory


@author:     COAL Developers

@copyright:  2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

#!/usr/bin/python

import os
import sys
import pycoal
sys.path.insert(0, '../pycoal')
import mineral
import fnmatch

#Path to EcoStress Spectral Library
if (len(sys.argv) == 1):
    raise Exception('Must pass in location of EcoStress Spectral Library')
library_filename = sys.argv[1]
#Loop through and edit all .spectrum.txt files
for root, dir, files in os.walk(library_filename):
    dir[:] = [d for d in dir]
    for items in fnmatch.filter(files, "*spectrum.txt"):
        input_file = open(library_filename + '/' + items, "r", encoding="utf8", errors='ignore')
        contents = input_file.readlines()
        input_file.close()
        #Add 5 '\n' after description
        contents.insert(11, '\n\n\n\n\n')
        input_file = open(library_filename + '/' + items, "w", encoding="utf8", errors='ignore')
        contents = "".join(contents)
        input_file.write(contents)
        input_file.close()
        #Edit vegation files because their format causes errors in the Spectral class
        if "vegetation" in items:
            input_file = open(library_filename + '/' + items, "r", encoding="utf8", errors='ignore')
            contents = input_file.readlines()
            input_file.close()
            #Add subclass and particle size
            contents.insert(5,'Subclass:\nParticle Size:   Unknown\n')
            #Remove Genus and Species
            contents.pop(4);
            contents.pop(3);
            input_file = open(library_filename + '/' + items, "w", encoding="utf8", errors='ignore')
            contents = "".join(contents)
            input_file.write(contents)
            input_file.close()

ecoStress = mineral.AsterConversion()
ecoStress.convert(library_filename,'dataEcoStress.db','ECO_01_SPLIB.envi')

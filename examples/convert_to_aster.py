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
convert_to_aster.py -- an example script to convert a USGS Spectral Library Version 7 file
to match the format of an ASTER Library Version 2.0 file

This class method converts a USGS Spectral version 7
<https://speclab.cr.usgs.gov/spectral-lib.html> .txt file into
an ASTER Library Version 2.0 <https://asterweb.jpl.nasa.gov/> .spectrum.txt file
ASTER Library Version 2.0 Spectral Library files are in .spectrum.txt file format

@author:     COAL Developers

@copyright:  2017-2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import os

#This will take the .txt files for Spectra in USGS Spectral Version 7 and convert
#their format to match that of ASTER .spectrum.txt files for spectra
library_filename = 'splib07a_Alizarin_crimson_(dk)_GDS780_ASDFRa_AREF.txt'
#Count amount of lines in library_filename
with open(library_filename,'r') as input_file:
    for line_count, l in enumerate(input_file):
        pass

input_file = open(library_filename,'r')
#Read Name of Spectra on first line of the file
spectra_line = input_file.readline()
spectra_name = spectra_line[23:]
k = 0
#Loop through file and store all wavelength values for the given Spectra
spectra_values_file = open('SpectraValues.txt','w')
while(k < line_count):
    spectra_wave_length = float(input_file.readline()) * 100
    spectra_wave_length = spectra_wave_length / 1000
    spectra_y_value = spectra_wave_length * 10
    line = str(spectra_wave_length) + '  ' + str(spectra_y_value)
    spectra_values_file.write(line)
    spectra_values_file.write('\n')
    k = k+1
#Write new file in the form of an ASTER .spectrum.txt file while using stored
#Spectra Name and stored Spectra Wavelength values`
input_file = open(library_filename,'w')
input_file.write('Name:')
input_file.write(spectra_name)
input_file.write('Type:\n')
input_file.write('Class:\n')
input_file.write('Subclass:\n')
input_file.write('Particle Size:  Solid\n')
input_file.write('Sample No.:  0095UUUASP\n')
input_file.write('Owner:\n')
input_file.write('Wavelength Range:  ALL\n')
input_file.write('Origin: Spectra obtained from the Noncoventional Exploitation Factors\n')
input_file.write('Data System of the National Photographic Interpretation Center.\n')
input_file.write('Description:  Gray and black construction asphalt.  The sample was\n')
input_file.write('soiled and weathered, with some limestone and quartz aggregate\n')
input_file.write('showing.\n')
input_file.write('\n')
input_file.write('\n')
input_file.write('\n')
input_file.write('Measurement:  Directional (10 Degree) Hemispherical Reflectance\n')
input_file.write('First Column:  X\n')
input_file.write('Second Column: Y\n')
input_file.write('X Units:  Wavelength (micrometers)\n')
input_file.write('Y Units:  Reflectance (percent)\n')
input_file.write('First X Value:\n')
input_file.write('Last X Value:\n')
input_file.write('Number of X Values:\n')
input_file.write('Additional Information:\n')
input_file.write('\n')
j = 0
spectra_values_file.close()
#Read in values saved in SpectraValues.txt and output them to the library_filename
spectra_values_file = open('SpectraValues.txt','r')
while(j < line_count):
    spectra_wave_length = spectra_values_file.readline()
    input_file.write(spectra_wave_length)
    j = j+1
#Close all open files
input_file.close()
spectra_values_file.close()
#Rename library_filename to match ASTER .spectrum.txt file format
os.rename(library_filename,library_filename + '.spectrum.txt')
#Remove temporary file for storing wavelength data
os.remove('SpectraValues.txt')
print("Successfully converted file " + library_filename)

#!/usr/bin/python
#
# Copyright (C) 2018 COAL Developers
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
Spectral Version 7 .txt file converted to ASTER .txt file format

@author:     COAL Developers

@copyright:  2018 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys
import os
from sys import path
from os import getcwd
import inspect
import math
import numpy

#This will convert a Spectral Version .txt file to a ASTER .txt file
library_filename = 'splib07a_Alizarin_crimson_(dk)_GDS780_ASDFRa_AREF.txt'
with open(library_filename,'r') as f:
    for i, l in enumerate(f):
        pass

f = open(library_filename,'r')
nameTemp = f.readline()
name = nameTemp[23:]
k = 0
x = open('2.txt','w')
while(k < i):
    num = float(f.readline()) * 100
    num = num / 1000
    num2 = num * 10
    num = round(num,4)
    num2 = round(num2,4)
    line = str(num) + '  ' + str(num2)
    x.write(line)
    x.write('\n')
    k = k+1
f = open(library_filename,'w')
f.write('Name:')
f.write(name)
f.write('Type:\n')
f.write('Class:\n')
f.write('Subclass:\n')
f.write('Particle Size:  Solid\n')
f.write('Sample No.:  0095UUUASP\n')
f.write('Owner:\n')
f.write('Wavelength Range:  ALL\n')
f.write('Origin: Spectra obtained from the Noncoventional Exploitation Factors\n')
f.write('Data System of the National Photographic Interpretation Center.\n')
f.write('Description:  Gray and black construction asphalt.  The sample was\n')
f.write('soiled and weathered, with some limestone and quartz aggregate\n')
f.write('showing.\n')
f.write('\n')
f.write('\n')
f.write('\n')
f.write('Measurement:  Directional (10 Degree) Hemispherical Reflectance\n')
f.write('First Column:  X\n')
f.write('Second Column: Y\n')
f.write('X Units:  Wavelength (micrometers)\n')
f.write('Y Units:  Reflectance (percent)\n')
f.write('First X Value:\n')
f.write('Last X Value:\n')
f.write('Number of X Values:\n')
f.write('Additional Information:\n')
f.write('\n')
j = 0
x.close()
x = open('2.txt','r')
while(j < i):
    num = x.readline()
    f.write(num)
    j = j+1
f.close()
x.close()
os.rename(library_filename,library_filename + '.spectrum.txt')
os.remove('2.txt')
print("Successfully converted file " + library_filename)



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

import logging

import sys
import os
from sys import path
from os import getcwd
import inspect
import pycoal
sys.path.insert(0, '../pycoal')
reload(sys)
sys.setdefaultencoding('utf8')
import mineral
import math
import numpy
import spectral
import glob

#This will convert a Spectral Version .txt file to a ASTER .txt file
library_filename = 'usgs_splib07_modified/'
# create a new mineral aster conversion instance
spectral_aster = mineral.SpectralToAsterConversion()
# Convert all files
files = os.listdir(library_filename)
for x in range(0, len(files)):
    name = 'usgs_splib07_modified/' + files[x]
    #print(name)
    spectral_aster.convert(name)



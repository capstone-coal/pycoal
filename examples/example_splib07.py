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
example_sam -- Plot Spectral Angles

.sli and .hdr files will be generated from spectral library.

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
import mineral
import math
import numpy
import spectral

# load library
spectral_library_file = '../pycoal/tests/usgs_splib07/ASCIIdata/splib07a_Bandpass_(FWHM)_ASDFR_StandardResolution.db'
header_name = "s07av95a_envi"

# create a new mineral aster conversion instance
spectral_envi = mineral.SpectralConversion()
# Generate .sli and .hdr
spectral_envi.convert(header_name,spectral_library_file)


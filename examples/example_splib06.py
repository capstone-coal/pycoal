# Copyright (C) 2017-2018 COAL Developers
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
example_splib06 -- Vizualizing the USGS Digital Spectral Library 06

The Spectral Python (SPy) library `provides<http://www.spectralpython.net/class_func_ref.html#spectral.view_cube>`_ the function ``view_cube`` to display a three-dimensional representation of an MxNxB hyperspectral image. Each face of the cube is MxB or NxB, where B is the number of bands. The USGS Digital Spectral Library 06 in AVIRIS-C format (SPLIB06) is an ENVI spectral library with 1365 samples and 224 bands each. This example demonstrates how to vizualize the library in the same way that SPy displays the sides of a hypercube.

The image ``s06av95a_envi.png`` is saved in the current directory. It shows that the library contains many sequentially similar samples, consistent with groupings of related class names. The horizontal black bars most prominent in far right samples are likely spectral ranges that were not detectable by the spectrometer. Each of the 1365 samples is represented by a pixel column from left to right. Each of the 224 bands is a pixel row, from near ultraviolet (0.38 micrometers) on the top to short-wave infrared (2.5 micrometers) on the bottom.

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2018 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import numpy
import spectral
from spectral.graphics.colorscale import create_default_color_scale

# Import SPLIB06 as a SPy image and display its dimensions.
library_filename = '../pycoal/tests/s06av95a_envi.hdr'
library = spectral.open_image(library_filename)
library.spectra.shape
# (1365, 224)

# Transpose the image to display vertical samples horizontally and display its dimensions.
spectra = numpy.transpose(library.spectra)
spectra.shape
# (224, 1365)

# Create a 256 color scale gradient.
scale = create_default_color_scale(256)

# Generate and display a Python Imaging Library (PIL) image. Arbitrarily scale the very small reflectance values by `50` to produce a suitable color distribution.
pilspectra = spectral.graphics.make_pil_image(50*spectra, color_scale=scale)
pilspectra.save('s06av95a_envi.png')

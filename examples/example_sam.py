#!/usr/bin/python
#
# Copyright (C) COAL Developers
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

The images ``sam.png`` and ``sam.svg`` are saved in the current directory.

@author:     COAL Developers

@copyright:  2017 COAL Developers. All rights reserved.

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import math
import numpy
import spectral
import matplotlib
import matplotlib.pyplot as plt

# load library
library_filename = '../pycoal/tests/s06av95a_envi.hdr'
library = spectral.open_image(library_filename)

# open the image
image_filename = '../pycoal/tests/images/ang20150422t163638_corr_v1e_img_4000-4010_550-560.hdr'

image = spectral.open_image(image_filename)

# access a pixel known
x = 4
y = 7
pixel = image[x,y]

# define a resampler
resample = spectral.BandResampler([x/1000 for x in image.bands.centers],
                                          library.bands.centers)

# resample the pixel
resampled_pixel = numpy.nan_to_num(resample(pixel))

# calculate spectral angles
angles = spectral.spectral_angles(resampled_pixel[numpy.newaxis,
                                                  numpy.newaxis,
                                                  ...],
                                  library.spectra)

# normalize confidence values from [pi,0] to [0,1]
for z in range(angles.shape[2]):
    angles[0,0,z] = 1-angles[0,0,z]/math.pi

# get angles, classes, and indices
angle_list = list(numpy.ndarray.flatten(angles))
angle_class_list = zip(angle_list, library.names, range(0,len(library.names)))
sorted_angle_class_list = sorted(angle_class_list, key=lambda x: x[0], reverse=True)
angle_list, class_list, index_list = zip(*sorted_angle_class_list)

# customize figure
plt.rcParams['font.size'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['text.color'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['figure.edgecolor'] = 'black'
plt.rcParams['savefig.facecolor'] = 'black'
plt.rcParams['savefig.edgecolor'] = 'black'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = 5.5,3.5
plt.rcParams['grid.color'] = 'white'

# generate figure
N = 15
ind = numpy.arange(N)
width = 0.70
plt.bar(ind, angle_list[0:N], width, color='orange', align='center')
plt.axhline(y=0.75, color='red')
plt.xticks(ind, index_list[0:N])
plt.title('Spectral Angles')
plt.xlabel('Spectral Library Index')
plt.ylabel('Confidence Value')
plt.xlim(-1,N)
plt.ylim(0,1)
plt.savefig('sam.png')
plt.savefig('sam.svg')

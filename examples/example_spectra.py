# Copyright (C) 2017-2019 COAL Developers
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
example_spectra -- Reflectance of Coal Mining Proxy Classes

The images ``spectra.png`` and ``spectra.svg`` are saved in the current directory.

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2019 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import constants
import spectral
import matplotlib
import matplotlib.pyplot as plt

# load library
library_filename = constants.LIBRARY_FILENAME
library = spectral.open_image(library_filename)
schwert_index = library.names.index(u'Schwertmannite BZ93-1 s06av95a=b')
sldgwet_index = library.names.index(u'Renyolds_TnlSldgWet SM93-15w s06av95a=a')
sludge_index  = library.names.index(u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a')
bands = [1000*band for band in library.bands.centers]

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
plt.plot(bands, library.spectra[schwert_index], 'orange', label=u'Schwertmannite BZ93-1 s06av95a=b')
plt.plot(bands, library.spectra[sludge_index], 'red', label=u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a')
plt.plot(bands, library.spectra[sldgwet_index], 'yellow', label=u'Renyolds_TnlSldgWet SM93-15w s06av95a=a')
plt.title('Reflectance of Coal Mining Proxy Classes')
plt.ylabel('Reflectance')
plt.xlabel('Wavelength (nm)')
plt.legend()
plt.axis([min(bands),max(bands),0,0.8])
plt.grid()
plt.savefig('spectra.png')
plt.savefig('spectra.svg')

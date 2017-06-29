=============
COAL Examples
=============

Welcome to the COAL examples directory. Here you will find helpful example scripts enabling you to run and experiment with all COAL functionality. The example here are based entirely off of the `usage <https://capstone-coal.github.io/docs#usage>`__ scenarios provided over at the main COAL Website.

Please report any issues you find here over at the `pycoal issue tracker <https://github.com/capstone-coal/pycoal/issues>`__ `labeling <https://github.com/capstone-coal/pycoal/labels>`__ your issue appropriately using **examples** and then the type of issue you are having e.g. **help wanted**, **question**, etc.

Prerequisites
-------------

AVIRIS-NG Data
^^^^^^^^^^^^^^
pycoal does not come packaged with absolutely everything e.g. spectral library(ies), input hyperspectral spectroscopy data, etc. In order to run the following examples, you need to download AVIRIS data to the **examples** directory. N.B. This data may take a significant amount of time to download depending on your network... go and make yourself a cup of tea or two!

::

	wget -m "ftp://avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2/ang20150420t182050_rfl_v1e/"

A full description of what this data actually is, is detailed in the `AVIRIS-NG Distribution Document <ftp://avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2/ang20150420t182050_rfl_v1e/ang20150420t182050_v1e_README.txt>`__.

USGS Digital Spectral Library splib06a
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In this directory, you will also notice a file named **s06av95a_envi.hdr**. This, as explained in the example, is the `USGS Digital Spectral Library splib06a <https://speclab.cr.usgs.gov/spectral.lib06/ds231/index.html>`__ we use to characterize and classify AVIRIS pixel spectral signatures.

Mineral Classification
----------------------
The Mineral Classification API provides methods for generating visible-light and mineral classified images. Mineral classification can take hours to days depending on the size of the spectral library and the available computing resources, so running a script in the background is recommended.

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

::

	usage: example_mineral.py [-h] [-i INPUT] [-l SLIB]

	example_mineral -- an example script which demonstrates COAL mineral classification

	VERSION 0.5.2

	Copyright 2017 COAL Developers. All rights reserved.

	This program is free software; you can redistribute it and/or 
	modify it under the terms of the GNU General Public License 
	as published by the Free Software Foundation; version 2.

	This program is distributed in the hope that it will be useful, 
	but WITHOUT ANY WARRANTY; without even the implied warranty 
	of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public 
	License along with this program; if not, write to the Free 
	Software Foundation, Inc., 51 Franklin Street, Fifth 
	Floor, Boston, MA 02110-1301, USA.

	USAGE

	optional arguments:
		-h, --help            	show this help message and exit
		-i INPUT, --input INPUT
                        		Input file to be processed [default:
                        		ang20150420t182050_corr_v1e_img.hdr
		-l SLIB, --slib SLIB  	Spectral Library filename [default: s06av95a_envi.hdr]

After running this Python script, you will see two new images written locally, namely

 * **ang20150420t182050_corr_v1e_img_rgb.hdr** - a visible-light image, and
 * **ang20150420t182050_corr_v1e_img_class.hdr** - a mineral classified image

Mining Classification
---------------------

 ...

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

 ...

Environment Classification
--------------------------

 ...

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

 ...

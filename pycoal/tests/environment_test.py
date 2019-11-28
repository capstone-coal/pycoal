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

from nose import with_setup
import test

from os.path import abspath, basename, splitext
import numpy
import spectral
import pycoal
from pycoal import environment

# Create test images with QGIS and GDAL by creating a cutline and using it to
# crop raster and vector files.
#
# To create a cutline in QGIS, go to Layer > New > New Shapefile Layer, select
# its type as Polygon and choose an output file, Toggle Editing, Add Feature to
# draw a bounding box, and finally Save the result.
#
# To create a raster test image with GDAL, run
# $ gdalwarp -of envi \
#            -crop_to_cutline \
#            -cutline cutline.shp \
#            input.img \
#            output.img
# Then edit the output header file to include the classification data from the
# input file.
#
# To create a vector test image with QGIS, go to Vector > Geoprocessing Tools >
# Clip and choose the input, clip, and output layers.

# test files for proximity intersection test
mining_filename = 'images/ang20150420t182050_corr_v1e_img_class_mining_cut.hdr'
vector_filename = ['images/NHDFlowline_cut.shp']
proximity = 10.0
correlated_filename = 'images' \
                      '/ang20150420t182050_corr_v1e_img_class_mining_cut' \
                      '_NHDFlowline_corr.hdr'
test_filename = 'images' \
                '/ang20150420t182050_corr_v1e_img_class_mining_cut' \
                '_NHDFlowline_corr_test.hdr'


# remove generated files
def _test_intersect_proximity_teardown():
    mining_name = splitext(basename(abspath(mining_filename)))[0]
    for vector_file in vector_filename:
    	vector_name = splitext(basename(abspath(vector_file)))[0]
    	output_directory = 'images'
    	feature_header_name = output_directory + '/' + mining_name + '_' + \
        	vector_name + '.hdr'
    	feature_image_name = feature_header_name[:-4] + '.img'
    	proximity_header_name = output_directory + '/' + mining_name + '_' + \
        	vector_name + '_proximity.hdr'
    	proximity_image_name = proximity_header_name[:-4] + '.img'
    	test_image_name = test_filename[:-4] + '.img'
    	test.remove_files(
        	[feature_header_name, feature_image_name, proximity_header_name,
         	proximity_image_name, test_filename, test_image_name])


# verify that proximity intersection produces expected results
@with_setup(None, _test_intersect_proximity_teardown)
def test_intersect_proximity():
    ec = environment.EnvironmentalCorrelation()
    ec.intersect_proximity(mining_filename, vector_filename, proximity,
                           test_filename)
    expected = spectral.open_image(correlated_filename)
    actual = spectral.open_image(test_filename)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert actual.metadata.get(
        'description') == 'COAL ' + pycoal.version + ' environmental ' \
                                                     'correlation image.'
    assert expected.metadata.get('class names') == actual.metadata.get(
        'class names')
    assert expected.metadata.get('map info') == actual.metadata.get('map info')


# set up test module before running tests
def setup_module():
    test.setup_module()


# tear down test module after running tests
def teardown_module():
    test.teardown_module()

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nose import with_setup
from unittest import skipIf
from test import setup_module, teardown_module, _remove_files

from os import environ
from os.path import abspath, dirname, basename, splitext
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
miningFilename = 'images/ang20150420t182050_corr_v1e_img_class_mining_cut.hdr'
vectorFilename = 'images/NHDFlowline_cut.shp'
proximity = 10.0
correlatedFilename = 'images/ang20150420t182050_corr_v1e_img_class_mining_cut_NHDFlowline_corr.hdr'
testFilename = 'images/ang20150420t182050_corr_v1e_img_class_mining_cut_NHDFlowline_corr_test.hdr'

# remove generated files
def _test_intersectProximity_teardown():
    miningName = splitext(basename(abspath(miningFilename)))[0]
    vectorName = splitext(basename(abspath(vectorFilename)))[0]
    outputDirectory = 'images'
    featureHeaderName = outputDirectory + '/' + miningName + '_' + vectorName + '.hdr'
    featureImageName = featureHeaderName[:-4] + '.img'
    proximityHeaderName = outputDirectory + '/' + miningName + '_' + vectorName + '_proximity.hdr'
    proximityImageName = proximityHeaderName[:-4] + '.img'
    testImageName = testFilename[:-4] + '.img'
    _remove_files([featureHeaderName, featureImageName,
                   proximityHeaderName, proximityImageName,
                   testFilename, testImageName])

# verify that proximity intersection produces expected results
@with_setup(None, _test_intersectProximity_teardown)
@skipIf(environ.get('CONTINUOUS_INTEGRATION'), 'Skip test because GDAL not installed on server.')
def test_intersectProximity():
    ec = environment.EnvironmentalCorrelation()
    ec.intersectProximity(miningFilename, vectorFilename, proximity, testFilename)
    expected = spectral.open_image(correlatedFilename)
    actual = spectral.open_image(testFilename)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert actual.metadata.get('description') == 'PyCOAL '+pycoal.version+' environmental correlation image.'
    assert expected.metadata.get('class names') == actual.metadata.get('class names')
    assert expected.metadata.get('map info') == actual.metadata.get('map info')

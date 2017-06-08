# Copyright (C) 2017 COAL Developers
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
from test import setup_module, teardown_module, _remove_files

import numpy
import spectral
import pycoal
import pycoal.mining

# test files for mining classification test
mineralFilename = 'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.hdr'
miningFilename = 'images/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80.hdr'
testFilename = 'images/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80_test.hdr'
testImage = 'images/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80_test.img'

# delete temporary files
def _test_classifyImage_teardown():
    _remove_files([testFilename, testImage])

# verify that the expected mining classifications equal the actual mining classifications
@with_setup(None, _test_classifyImage_teardown)
def test_classifyImage():

    # classify mining and and save to temporary file
    mc = pycoal.mining.MiningClassification()
    mc.classifyImage(mineralFilename, testFilename)

    # open the mining and temporary files
    expected = spectral.open_image(miningFilename)
    actual = spectral.open_image(testFilename)

    # verify that every pixel has the same classification
    assert numpy.array_equal(expected.asarray(), actual.asarray())

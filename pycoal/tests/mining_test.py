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

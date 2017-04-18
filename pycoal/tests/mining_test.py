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

import os
import numpy
import spectral
import pycoal
import pycoal.mining

# filename of 10x10 mineral subimage
mineralFilename = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.hdr'

# filename of 10x10 mining subimage
miningFilename = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80.hdr'

# filenames of temporary files
testFilename = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80_test.hdr'
testImage = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_mining_4200-4210_70-80_test.img'

# delete temporary files
def _test_classifyImage_teardown():
    try:
        os.remove(testFilename)
        os.remove(testImage)
    except OSError:
        pass

# verify that the expected mining classifications equal the actual mining classifications
@with_setup(None, _test_classifyImage_teardown)
def test_classifyImage():

    # classify mining and and save to temporary file
    mc = pycoal.mining.MiningClassification([u'Schwertmannite BZ93-1 s06av95a=b', u'Renyolds_TnlSldgWet SM93-15w s06av95a=a', u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a'])
    mc.classifyImage(mineralFilename, testFilename)

    # open the mining and temporary files
    expected = spectral.open_image(miningFilename)
    actual = spectral.open_image(testFilename)

    # verify that every pixel has the same classification
    assert numpy.array_equal(expected.asarray(), actual.asarray())

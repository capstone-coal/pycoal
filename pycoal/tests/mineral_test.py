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
import shutil
import numpy
import spectral
import pycoal
import pycoal.mineral

# test files for filterClasses test
test_filterClasses_Filename = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.hdr'
test_filterClasses_Image = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.img'
test_filterClasses_testFilename = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80_filtered.hdr'
test_filterClasses_testImage = 'pycoal/tests/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80_filtered.img'

# set up filterClasses test by copying classified image
def _test_filterClasses_setup():
    shutil.copyfile(test_filterClasses_Filename, test_filterClasses_testFilename)
    shutil.copyfile(test_filterClasses_Image, test_filterClasses_testImage)

# tear down filterClasses test by deleting filtered image
def _test_filterClasses_teardown():
    try:
        os.remove(test_filterClasses_testFilename)
        os.remove(test_filterClasses_testImage)
    except OSError:
        pass

# verify that filterClasses removes unused classes and reindexes correctly
@with_setup(_test_filterClasses_setup, _test_filterClasses_teardown)
def test_filterClasses():
    pycoal.mineral.MineralClassification.filterClasses(test_filterClasses_testFilename)
    original = spectral.open_image(test_filterClasses_Filename)
    filtered = spectral.open_image(test_filterClasses_testFilename)
    assert int(filtered.metadata.get('classes')) == len(set(original.asarray().flatten().tolist()))
    for x in range(original.shape[0]):
        for y in range(original.shape[1]):
            originalClassName = original.metadata.get('class names')[original[x,y,0]]
            filteredClassName = filtered.metadata.get('class names')[filtered[x,y,0]]
            assert originalClassName == filteredClassName

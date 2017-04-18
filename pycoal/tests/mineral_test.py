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
import pycoal.mineral

# filename of 1x1 subimage
test_toRGB_imageFilename = 'pycoal/tests/ang20150422t163638_corr_v1e_img_987_654.hdr'

# filename of 1x1 RGB subimage
test_toRGB_rgbFilename = 'pycoal/tests/ang20150422t163638_corr_v1e_img_987_654_rgb.hdr'

# filenames of temporary files
test_toRGB_testFilename = 'pycoal/tests/ang20150422t163638_corr_v1e_img_987_654_rgb_test.hdr'
test_toRGB_testImage = 'pycoal/tests/ang20150422t163638_corr_v1e_img_987_654_rgb_test.img'

# delete temporary files
def _test_toRGB_teardown():
    try:
        os.remove(test_toRGB_testFilename)
        os.remove(test_toRGB_testImage)
    except OSError:
        pass

# verify that the RGB converter selects the correct bands and updates the metadata
@with_setup(None, _test_toRGB_teardown)
def test_toRGB():
    pycoal.mineral.MineralClassification.toRGB(test_toRGB_imageFilename, test_toRGB_testFilename)
    expected = spectral.open_image(test_toRGB_rgbFilename)
    actual = spectral.open_image(test_toRGB_testFilename)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert expected.metadata.get('wavelength') == actual.metadata.get('wavelength')
    assert expected.metadata.get('correction factors') == actual.metadata.get('correction factors')
    assert expected.metadata.get('fwhm') == actual.metadata.get('fwhm')
    assert expected.metadata.get('bbl') == actual.metadata.get('bbl')
    assert expected.metadata.get('smoothing factors') == actual.metadata.get('smoothing factors')

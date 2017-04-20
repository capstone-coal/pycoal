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

# test files for the classifyImage test
test_classifyImage_testFilename_1 = "pycoal/tests/ang20140912t192359_corr_v1c_img_400-410_10-20.hdr"
test_classifyImage_classifiedFilename_1 = "pycoal/tests/ang20140912t192359_corr_v1c_img_400-410_10-20_class.hdr"

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

# filename of 1x1 subimage
test_toRGB_AVC_imageFilename = 'pycoal/tests/f080702t01p00r08rdn_c_sc01_ort_img_123_456.hdr'

# filename of 1x1 RGB subimage
test_toRGB_AVC_rgbFilename = 'pycoal/tests/f080702t01p00r08rdn_c_sc01_ort_img_123_456_rgb.hdr'

# filenames of temporary files
test_toRGB_AVC_testFilename = 'pycoal/tests/f080702t01p00r08rdn_c_sc01_ort_img_rgb_test.hdr'
test_toRGB_AVC_testImage = 'pycoal/tests/f080702t01p00r08rdn_c_sc01_ort_img_rgb_test.img'

# delete temporary files
def _test_toRGB_AVC_teardown():
    try:
        os.remove(test_toRGB_AVC_testFilename)
        os.remove(test_toRGB_AVC_testImage)
    except OSError:
        pass

# verify that the RGB converter selects the correct bands and updates the metadata
@with_setup(None, _test_toRGB_AVC_teardown)
def test_toRGB_AVC():
    pycoal.mineral.MineralClassification.toRGB(test_toRGB_AVC_imageFilename, test_toRGB_AVC_testFilename)
    expected = spectral.open_image(test_toRGB_AVC_rgbFilename)
    actual = spectral.open_image(test_toRGB_AVC_testFilename)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert expected.metadata.get('wavelength') == actual.metadata.get('wavelength')
    assert expected.metadata.get('correction factors') == actual.metadata.get('correction factors')
    assert expected.metadata.get('fwhm') == actual.metadata.get('fwhm')
    assert expected.metadata.get('bbl') == actual.metadata.get('bbl')
    assert expected.metadata.get('smoothing factors') == actual.metadata.get('smoothing factors')


# verify that classified images have valid classifications
def test_classifyImage():
    # TODO: get correct download link
    lib = "/home/claytonh/Downloads/USGS/s06av95a_envi.hdr"

    tst_cls = pycoal.mineral.MineralClassification(lib)

    # make sure library is being opened as such
    assert isinstance(tst_cls.library, spectral.io.envi.SpectralLibrary)

    tst_cls.classifyImage(test_classifyImage_testFilename_1, test_classifyImage_classifiedFilename_1)

    classified = spectral.open_image(test_classifyImage_classifiedFilename_1)

    # access classified pixels
    cls_memmap = classified.open_memmap()

    # assert there are no invalid class numbers
    for i in cls_memmap:
        for j in i:
            assert 0 <= j[0] <= len(tst_cls.library.names) + 1

    # TODO: generate two more test images


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
from nose.tools import assert_raises
import test

import shutil
import os
import numpy
import spectral
import pycoal
import unittest
from pycoal import conversion
from pycoal import mineral
from pycoal import mining

# To create test images with Spectral Python, run
# > spectral.envi.save_image('image_x0-xn_y0-yn.hdr', \
#                            image[x0:xn,y0:yn,:], \
#                            metadata=image.metadata)

# test files for classifyImage tests
# TODO test AVIRIS-C
test_classifyImage_testFilenames = [
    "images/ang20140912t192359_corr_v1c_img_400-410_10-20.hdr",
    "images/ang20140912t192359_corr_v1c_img_2580-2590_540-550.hdr",
    "images/ang20150422t163638_corr_v1e_img_4000-4010_550-560.hdr"]


# delete temporary files for classifyImage tests
def _test_classify_image_teardown():
    test.remove_files([f[:-4] + '_class_test.hdr' for f in
                       test_classifyImage_testFilenames] + [
                          f[:-4] + '_class_test.img' for f in
                          test_classifyImage_testFilenames])

@with_setup(None, _test_classify_image_teardown)
def test_config_file_wrong_algo():
    # create mineral classifier instance, should raise keyerror
    # in __init__ due to no MAS_pytorch function in globals array
    config = 'tests/test_config_files/config_test_wrong_algo.ini'
    with assert_raises(KeyError):
        _mc = mineral.MineralClassification(
            library_file_name=test.libraryFilenames[0],
            config_file = config
            )

@with_setup(None, _test_classify_image_teardown)
def test_config_file_wrong_impl():
    # create mineral classifier instance, should raise keyerror
    # in __init__ due to no SAM_p function in globals array
    config = 'tests/test_config_files/config_test_wrong_impl.ini'
    with assert_raises(KeyError):
        _mc = mineral.MineralClassification(
            library_file_name=test.libraryFilenames[0],
            config_file = config
            )
    
    

# verify that classified images have valid classifications
@with_setup(None, _test_classify_image_teardown)
def test_classify_image():
    # create mineral classifier instance
    mc = mineral.MineralClassification(
        library_file_name=test.libraryFilenames[0])

    # for each of the test images
    for image_file_name in test_classifyImage_testFilenames:
        # classify the test image
        classified_file_name = image_file_name[:-4] + "_class_test.hdr"
        mc.classify_image(image_file_name, classified_file_name)
        actual = spectral.open_image(classified_file_name)

        # classified image for comparison
        expected = spectral.open_image(image_file_name[:-4] + "_class.hdr")

        # validate metadata
        assert actual.metadata.get(
            u'description') == 'COAL ' + pycoal.version + ' mineral ' \
                                                          'classified image.'
        assert expected.metadata.get(u'file type') == actual.metadata.get(
            u'file type')
        assert expected.metadata.get(u'map info') == actual.metadata.get(
            u'map info')
        assert expected.metadata.get(u'class names') == actual.metadata.get(
            u'class names')
        assert expected.metadata.get(u'classes') == actual.metadata.get(
            u'classes')

        # verify that every pixel has the same classification
        assert numpy.array_equal(expected.asarray(), actual.asarray())
        
# verify that classified images have valid classifications
@with_setup(None, _test_classify_image_teardown)
def test_classify_image_config(config_filename):
    # create mineral classifier instance
    mc = mineral.MineralClassification()
        #config_file = config_filename),
        #library_file_name=test.libraryFilenames[0])
'''
    # for each of the test images
    for image_file_name in test_classifyImage_testFilenames:
        # classify the test image
        classified_file_name = image_file_name[:-4] + "_class_test.hdr"
        mc.classify_image(image_file_name, classified_file_name)
        actual = spectral.open_image(classified_file_name)

        # classified image for comparison
        expected = spectral.open_image(image_file_name[:-4] + "_class.hdr")

        # validate metadata
        assert actual.metadata.get(
            u'description') == 'COAL ' + pycoal.version + ' mineral ' \
                                                          'classified image.'
        assert expected.metadata.get(u'file type') == actual.metadata.get(
            u'file type')
        assert expected.metadata.get(u'map info') == actual.metadata.get(
            u'map info')
        assert expected.metadata.get(u'class names') == actual.metadata.get(
            u'class names')
        assert expected.metadata.get(u'classes') == actual.metadata.get(
            u'classes')

        # verify that every pixel has the same classification
        assert numpy.array_equal(expected.asarray(), actual.asarray())
'''

# verify that classified images have valid classifications when using config file
# three basic tests w/ diff parallel methods and loading image in mem

@unittest.skip("SAM_pytorch not implemented in branch")
@with_setup(None, _test_classify_image_teardown)
def test_classify_image_pytorch():
    # use our test config file with algo set to pytorch
    config = 'tests/test_config_files/config_test.ini'
    test_classify_image_config(config)
    test_classify_image_in_memory_config(config)

@unittest.skip("SAM_joblib not implemented in branch")
@with_setup(None, _test_classify_image_teardown)
def test_classify_image_joblib(config):
    # use our test config file with algo set to joblib
    config = 'tests/test_config_files/config_test_joblib.ini'
    test_classify_image_config(config)
    test_classify_image_in_memory_config(config)

    
# verify classification when loading entire images into memory
@with_setup(None, _test_classify_image_teardown)
def test_classify_image_in_memory():
    # create mineral classifier instance with image loading enabled
    mc = mineral.MineralClassification(
        library_file_name=test.libraryFilenames[0], in_memory=True)

    # for each of the test images
    for image_file_name in test_classifyImage_testFilenames:
        # classify the test image
        classified_file_name = image_file_name[:-4] + "_class_test.hdr"
        mc.classify_image(image_file_name, classified_file_name)
        actual = spectral.open_image(classified_file_name)

        # classified image for comparison
        expected = spectral.open_image(image_file_name[:-4] + "_class.hdr")

        # verify that every pixel has the same classification
        assert numpy.array_equal(expected.asarray(), actual.asarray())
        
# verify classification when loading entire images into memory
@with_setup(None, _test_classify_image_teardown)
def test_classify_image_in_memory_config(config_filename):
    # create mineral classifier instance with image loading enabled
    mc = mineral.MineralClassification(
         config_filename=config_filename, library_file_name=test.libraryFilenames[0], in_memory=True)

    # for each of the test images
    for image_file_name in test_classifyImage_testFilenames:
        # classify the test image
        classified_file_name = image_file_name[:-4] + "_class_test.hdr"
        mc.classify_image(image_file_name, classified_file_name)
        actual = spectral.open_image(classified_file_name)

        # classified image for comparison
        expected = spectral.open_image(image_file_name[:-4] + "_class.hdr")

        # verify that every pixel has the same classification
        assert numpy.array_equal(expected.asarray(), actual.asarray())


# test files for classify image threshold and subset tests
test_classifyImage_threshold_subset_imageFilename = \
    'images/ang20150420t182808_corr_v1e_img_4200-4210_70-80.hdr'
test_classifyImage_threshold_subset_testFilename = \
    'images/ang20150420t182808_corr_v1e_img_4200-4210_70-80_class_test.hdr'
test_classifyImage_threshold_subset_testImage = \
    'images/ang20150420t182808_corr_v1e_img_4200-4210_70-80_class_test.img'
test_classifyImage_threshold_subset_classifiedFilename = \
    'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.hdr'


# tear down classify image subset test by deleting classified file
def _test_classify_image_threshold_subset_teardown():
    test.remove_files([test_classifyImage_threshold_subset_testFilename,
                       test_classifyImage_threshold_subset_testImage])


# verify that threshold classification gives either the same result or no
# data for each pixel
@with_setup(None, _test_classify_image_threshold_subset_teardown)
def test_classify_image_threshold():
    # create mineral classification instance with threshold
    mc = mineral.MineralClassification(
        library_file_name=test.libraryFilenames[0], threshold=0.75)

    # classify image
    mc.classify_image(test_classifyImage_threshold_subset_imageFilename,
                      test_classifyImage_threshold_subset_testFilename)
    actual = spectral.open_image(
        test_classifyImage_threshold_subset_testFilename)

    # compare expected to actual classifications
    expected = spectral.open_image(
        test_classifyImage_threshold_subset_classifiedFilename)
    for x in range(actual.shape[0]):
        for y in range(actual.shape[1]):
            actual_class_id = actual[x, y, 0]
            actual_class_name = actual.metadata.get('class names')[
                actual_class_id]
            expected_class_id = expected[x, y, 0]
            expected_class_name = expected.metadata.get('class names')[
                expected_class_id]
            assert actual_class_name in (expected_class_name, 'No data')


# verify that subset classification identifies only the selected classes
@with_setup(None, _test_classify_image_threshold_subset_teardown)
def test_classify_image_subset():
    # create mineral classification instance with mining subset
    mc = mineral.MineralClassification(
        library_file_name=test.libraryFilenames[0],
        class_names=mining.PROXY_CLASS_NAMES_USGSV6)

    # classify image
    mc.classify_image(test_classifyImage_threshold_subset_imageFilename,
                      test_classifyImage_threshold_subset_testFilename)
    actual = spectral.open_image(
        test_classifyImage_threshold_subset_testFilename)

    # inspect the classifications
    for x in range(actual.shape[0]):
        for y in range(actual.shape[1]):
            actual_class_id = actual[x, y, 0]
            actual_class_name = actual.metadata.get('class names')[
                actual_class_id]
            assert actual_class_name in mining.PROXY_CLASS_NAMES_USGSV6 or \
                   actual_class_name == 'No data'


# test files for filter_classes test
test_filterClasses_Filename = \
    'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.hdr'
test_filterClasses_Image = \
    'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80.img'
test_filterClasses_testFilename = \
    'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80_filtered.hdr'
test_filterClasses_testImage = \
    'images/ang20150420t182808_corr_v1e_img_class_4200-4210_70-80_filtered.img'


# set up filter_classes test by copying classified image
def _test_filter_classes_setup():
    shutil.copyfile(test_filterClasses_Filename,
                    test_filterClasses_testFilename)
    shutil.copyfile(test_filterClasses_Image, test_filterClasses_testImage)


# tear down filter_classes test by deleting filtered image
def _test_filter_classes_teardown():
    test.remove_files(
        [test_filterClasses_testFilename, test_filterClasses_testImage])


# verify that filter_classes removes unused classes and reindexes correctly
@with_setup(_test_filter_classes_setup, _test_filter_classes_teardown)
def test_filter_classes():
    mineral.MineralClassification.filter_classes(
        test_filterClasses_testFilename)
    original = spectral.open_image(test_filterClasses_Filename)
    filtered = spectral.open_image(test_filterClasses_testFilename)
    assert int(filtered.metadata.get('classes')) == len(
        set(original.asarray().flatten().tolist()))
    for x in range(original.shape[0]):
        for y in range(original.shape[1]):
            original_class_name = original.metadata.get('class names')[
                original[x, y, 0]]
            filtered_class_name = filtered.metadata.get('class names')[
                filtered[x, y, 0]]
            assert original_class_name == filtered_class_name


# test files for AVIRIS-NG toRGB test
test_to_rgb_image_file_name = \
    'images/ang20150422t163638_corr_v1e_img_987_654.hdr'
test_to_rgb_rgb_file_name = \
    'images/ang20150422t163638_corr_v1e_img_987_654_rgb.hdr'
test_to_rgb_test_file_name = \
    'images/ang20150422t163638_corr_v1e_img_987_654_rgb_test.hdr'
test_toRGB_testImage = \
    'images/ang20150422t163638_corr_v1e_img_987_654_rgb_test.img'


# tear down AVIRIS-NG toRGB test by deleting temporary files
def _test_to_rgb_teardown():
    test.remove_files([test_to_rgb_test_file_name, test_toRGB_testImage])


# verify that the RGB converter selects the correct AVIRIS-NG bands and
# updates the metadata
@with_setup(None, _test_to_rgb_teardown)
def test_to_rgb():
    mineral.MineralClassification.to_rgb(test_to_rgb_image_file_name,
                                         test_to_rgb_test_file_name)
    expected = spectral.open_image(test_to_rgb_rgb_file_name)
    actual = spectral.open_image(test_to_rgb_test_file_name)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert expected.metadata.get('wavelength') == actual.metadata.get(
        'wavelength')
    assert expected.metadata.get('correction factors') == actual.metadata.get(
        'correction factors')
    assert expected.metadata.get('fwhm') == actual.metadata.get('fwhm')
    assert expected.metadata.get('bbl') == actual.metadata.get('bbl')
    assert expected.metadata.get('smoothing factors') == actual.metadata.get(
        'smoothing factors')


# test files for AVIRIS-C toRGB test
test_toRGB_AVC_imageFilename = \
    'images/f080702t01p00r08rdn_c_sc01_ort_img_123_456.hdr'
test_toRGB_AVC_rgbFilename = \
    'images/f080702t01p00r08rdn_c_sc01_ort_img_123_456_rgb.hdr'
test_toRGB_AVC_testFilename = \
    'images/f080702t01p00r08rdn_c_sc01_ort_img_rgb_test.hdr'
test_toRGB_AVC_testImage = \
    'images/f080702t01p00r08rdn_c_sc01_ort_img_rgb_test.img'


# tear down AVIRIS-C toRGB test by deleting temporary files
def _test_to_rgb_avc_teardown():
    test.remove_files([test_toRGB_AVC_testFilename, test_toRGB_AVC_testImage])


# verify that the RGB converter selects the correct AVIRIS-C bands and
# updates the metadata
@with_setup(None, _test_to_rgb_avc_teardown)
def test_to_rgb_avc():
    mineral.MineralClassification.to_rgb(test_toRGB_AVC_imageFilename,
                                         test_toRGB_AVC_testFilename)
    expected = spectral.open_image(test_toRGB_AVC_rgbFilename)
    actual = spectral.open_image(test_toRGB_AVC_testFilename)
    assert numpy.array_equal(expected.asarray(), actual.asarray())
    assert expected.metadata.get('wavelength') == actual.metadata.get(
        'wavelength')
    assert expected.metadata.get('correction factors') == actual.metadata.get(
        'correction factors')
    assert expected.metadata.get('fwhm') == actual.metadata.get('fwhm')
    assert expected.metadata.get('bbl') == actual.metadata.get('bbl')
    assert expected.metadata.get('smoothing factors') == actual.metadata.get(
        'smoothing factors')


# test files for AVIRIS-NG no data toRGB test
test_toRGB_noData_imageFilename = \
    'images/ang20140912t192359_corr_v1c_img_400-410_10-20.hdr'
test_toRGB_noData_rgbFilename = \
    'images/ang20140912t192359_corr_v1c_img_400-410_10-20_rgb.hdr'
test_toRGB_noData_testFilename = \
    'images/ang20140912t192359_corr_v1c_img_400-410_10-20_rgb_test.hdr'
test_toRGB_noData_testImage = \
    'images/ang20140912t192359_corr_v1c_img_400-410_10-20_rgb_test.img'


# tear down AVIRIS-NG no data toRGB test
def _test_to_rgb_no_data_teardown():
    test.remove_files(
        [test_toRGB_noData_testFilename, test_toRGB_noData_testImage])


# verify that AVIRIS-NG images with no data pixels are converted to RGB
# TODO test AVIRIS-C
@with_setup(None, _test_to_rgb_no_data_teardown)
def test_to_rgb_no_data():
    mineral.MineralClassification.to_rgb(test_toRGB_noData_imageFilename,
                                         test_toRGB_noData_testFilename)
    expected = spectral.open_image(test_toRGB_noData_rgbFilename)
    actual = spectral.open_image(test_toRGB_noData_testFilename)
    assert actual.metadata.get('data ignore value') == '0'
    assert numpy.array_equal(expected.asarray(), actual.asarray())


# test files for ASTER conversion test
_test_AsterConversion_data = 'ASTER/data'
_test_AsterConversion_db = 'ASTER-2.0.db'
_test_AsterConversion_envi = 'ASTER-2.0'


# tear down ASTER conversion test by deleting test files
def _test_aster_conversion_teardown():
    test.remove_files(
        [_test_AsterConversion_db, _test_AsterConversion_envi + '.hdr',
         _test_AsterConversion_envi + '.sli'])


# verify that a small subset of the ASTER Spectral Library 2.0 is converted
# to ENVI format
@with_setup(None, _test_aster_conversion_teardown)
def test_aster_conversion():
    data, db, envi = _test_AsterConversion_data, _test_AsterConversion_db, \
                     _test_AsterConversion_envi
    aster_conversion = conversion.AsterToENVIConversion()
    assert_raises(ValueError, aster_conversion.convert, data_dir=data)
    assert_raises(ValueError, aster_conversion.convert, data_dir=data,
                  hdr_file=envi)
    assert_raises(ValueError, aster_conversion.convert, data_dir=data,
                  db_file=db)
    aster_conversion.convert(data_dir=data, db_file=db, hdr_file=envi)
    aster = spectral.open_image(envi + '.hdr')
    assert isinstance(aster, spectral.io.envi.SpectralLibrary)
    assert aster.spectra.shape == (3, 128)


# test files for FullSpectralLibrary7Convert conversion test
_test_SpectralConversion_data = 'usgs_splib07'
_test_SpectralConversion_dir = 'usgs_splib07_modified'
_test_SpectralConversion_db = 'dataSplib07.db'
_test_SpectralConversion_envi = 's07_AV95_envi_sample'
_test_SpectralConversion_envi_hdr = 's07_AV95_envi_sample.hdr'
_test_SpectralConversion_envi_sli = 's07_AV95_envi_sample.sli'


# tear down FullSpectralLibrary7Convert conversion test by deleting test files
def _test_spectral_conversion_teardown():
    test.remove_files(
        [_test_SpectralConversion_db, _test_SpectralConversion_dir,
         _test_SpectralConversion_envi, _test_SpectralConversion_envi_hdr,
         _test_SpectralConversion_envi_sli])


# verify that a small subset of the USGS Spectral Library 7 is converted to
# ENVI format
@with_setup(None, _test_spectral_conversion_teardown)
def test_spectral_conversion():
    data, envi = _test_SpectralConversion_data, _test_SpectralConversion_envi
    spectral_conversion = conversion.FullUSGSSpectral7ToENVIConversion()
    spectral_conversion.convert(library_filename=data)
    spectral7 = spectral.open_image(envi + '.hdr')
    assert isinstance(spectral7, spectral.io.envi.SpectralLibrary)
    if (os.path.isfile('SpectraValues.txt')):
        os.remove('SpectraValues.txt')
    shutil.rmtree('usgs_splib07_modified')


# set up test module before running tests
def setup_module():
    test.setup_module()


# tear down test module after running tests
def teardown_module():
    test.teardown_module()

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

import os
import logging
import math
import numpy
from spectral.io.spyfile import SubImage

import pycoal
import spectral
import time
import fnmatch
import shutil
import configparser
import errno

"""
Classifier callbacks functions must have at least the following args: library,
image_file_name, classified_file_name; which will always be passed by the
calling  method (MineralClassification.classify_image). The remaining
arguments, specific of each classifier function, will also be passed by the
calling function but are optionals and may vary from one classifier to another.
"""


def SAM(image_file_name, classified_file_name, library_file_name,
        scores_file_name=None, class_names=None, threshold=0.0,
        in_memory=False, subset_rows=None, subset_cols=None):
    """
    Parameter 'scores_file_name' optionally receives the path to where to save
    an image that holds all the SAM scores yielded for each pixel of the
    classified image. No score image is create if not provided.

    The optional 'threshold' parameter defines a confidence value between zero
    and one below which SAM classifications will be discarded, otherwise all
    classifications will be included.

    In order to improve performance on systems with sufficient memory,
    enable the optional parameter to load entire images.

    Args:
        library_file_name (str):            filename of the spectral library
        image_file_name (str):              filename of the image to be
                                            classified
        classified_file_name (str):         filename of the classified image
        scores_file_name (str, optional):   filename of the image to hold
                                            each pixel's classification score
        class_names (str[], optional):      list of classes' names to include
        threshold (float, optional):        classification threshold
        in_memory (boolean, optional):      enable loading entire image
        subset_rows (2-tuple, optional):    range of rows to read (empty
                                            to read the whole image)
        subset_cols (2-tuple, optional):    range of columns to read (
                                            empty to read the whole image)

    Returns:
        None
    """

    # load and optionally subset the spectral library
    library = spectral.open_image(library_file_name)
    if class_names is not None:
        library = pycoal.mineral.MineralClassification.subset_spectral_library(
            library, class_names)

    # open the image
    image = spectral.open_image(image_file_name)
    if subset_rows is not None and subset_cols is not None:
        subset_image = SubImage(image, subset_rows, subset_cols)
        m = subset_rows[1]
        n = subset_cols[1]
    else:
        if in_memory:
            data = image.load()
        else:
            data = image.asarray()
        m = image.shape[0]
        n = image.shape[1]

    logging.info("Classifying a %iX%i image" % (m, n))

    # define a resampler
    # TODO detect and scale units
    # TODO band resampler should do this
    resample = spectral.BandResampler([x / 1000 for x in image.bands.centers],
                                      library.bands.centers)

    # allocate a zero-initialized MxN array for the classified image
    classified = numpy.zeros(shape=(m, n), dtype=numpy.uint16)

    if scores_file_name is not None:
        # allocate a zero-initialized MxN array for the scores image
        scored = numpy.zeros(shape=(m, n), dtype=numpy.float64)

    # universal calculations for angles
    # Adapted from Spectral library
    angles_m = numpy.array(library.spectra, dtype=numpy.float64)
    angles_m /= numpy.sqrt(numpy.einsum('ij,ij->i', angles_m, angles_m))[:, numpy.newaxis]

    # for each pixel in the image
    for x in range(m):

        for y in range(n):

            # read the pixel from the file
            if subset_rows is not None and subset_cols is not None:
                pixel = subset_image.read_pixel(x, y)
            else:
                pixel = data[x, y]

            # if it is not a no data pixel
            if not numpy.isclose(pixel[0], -0.005) and not pixel[0] == -50:

                # resample the pixel ignoring NaNs from target bands that
                # don't overlap
                # TODO fix spectral library so that bands are in order
                resampled_pixel = numpy.nan_to_num(resample(pixel))

                # calculate spectral angles
                # Adapted from Spectral library
                resampled_data = resampled_pixel[numpy.newaxis, numpy.newaxis, ...]
                norms = numpy.sqrt(numpy.einsum('ijk,ijk->ij', resampled_data, resampled_data))
                dots = numpy.einsum('ijk,mk->ijm', resampled_data, angles_m)
                dots = numpy.clip(dots / norms[:, :, numpy.newaxis], -1, 1)
                angles = numpy.arccos(dots)

                # normalize confidence values from [pi,0] to [0,1]
                angles[0, 0, :] = 1 - angles[0, 0, :] / math.pi 

                # get index of class with largest confidence value
                index_of_max = numpy.argmax(angles)

                # get confidence value of the classified pixel
                score = angles[0, 0, index_of_max]

                # classify pixel if confidence above threshold
                if score > threshold:

                    # index from one (after zero for no data)
                    classified[x, y] = index_of_max + 1

                    if scores_file_name is not None:
                        # store score value
                        scored[x, y] = score

    # save the classified image to a file
    spectral.io.envi.save_classification(classified_file_name, classified,
                                         class_names=['No data'] +
                                         library.names,
                                         metadata={'data ignore value': 0,
                                                   'description': 'COAL ' +
                                                   pycoal.version + ' '
                                                   'mineral classified '
                                                   'image.',
                                                   'map info':
                                                       image.metadata.get(
                                                        'map info')})

    # remove unused classes from the image
    pycoal.mineral.MineralClassification.filter_classes(classified_file_name)

    if scores_file_name is not None:
        # save the scored image to a file
        spectral.io.envi.save_image(scores_file_name, scored,
                                    dtype=numpy.float64,
                                    metadata={'data ignore value': -50,
                                              'description': 'COAL ' +
                                              pycoal.version + ' mineral '
                                              'scored image.',
                                              'map info': image.metadata.get(
                                                  'map info')})


def avngDNN(image_file_name, classified_file_name, model_file_name,
            class_names=None, scores_file_name=None, in_memory=False):
    """
    This callback function takes a Keras model, trained to classify pixels
    from AVIRIS-NG
    imagery, and assigns a class for every single pixel of the input image.

    Parameter 'scores_file_name' optionally receives the path to where to save
    an image that holds all the SAM scores yielded for each pixel of the 
    classified image. No score image is create if not provided.

    In order to improve performance on systems with sufficient memory,
    enable the optional parameter to load entire images.

    Args:
        image_file_name (str):          filename of the image to be classified
        classified_file_name (str):     filename of the classified image
        model_file_name (str):          filename of the Keras model used to
        classify
        class_names (str[], optional):  list of names of classes handled by
        the model
        scores_file_name (str):         filename of the image to hold each
        pixel's classification score
        in_memory (boolean, optional):  enable loading entire image

    Returns:
        None
    """

    from keras.models import load_model

    # open the image
    image = spectral.open_image(image_file_name)
    if in_memory:
        data = image.load()
    else:
        data = image.asarray()
    m = image.shape[0]
    n = image.shape[1]

    # allocate a zero-initialized MxN array for the classified image
    classified = numpy.zeros(shape=(m, n), dtype=numpy.uint16)

    if scores_file_name is not None:
        # allocate a zero-initialized MxN array for the scores image
        scored = numpy.zeros(shape=(m, n), dtype=numpy.float64)

    model = load_model(model_file_name)

    # for each pixel in the image
    for x in range(m):

        for y in range(n):

            # read the pixel from the file
            pixel = numpy.array(data[x, y])

            # adjust shape to comprise the AVIRIS-NG bands and comply with
            # Keras model input format
            pixel = numpy.reshape(pixel, (1, 432, 1))

            # get the scores for each class considered
            predict = model.predict(pixel)

            # get the index of the class into the outputted list
            index_of_max = numpy.argmax(predict).astype(numpy.uint16)

            # store the class index (0 meaning nodata)
            classified[x, y] = index_of_max + 1

            # store the outcome score
            if scores_file_name is not None:
                scored[x, y] = predict[0][index_of_max]

    # save the classified image to a file
    spectral.io.envi.save_classification(classified_file_name, classified,
                                         class_names=['No data'] + class_names,
                                         metadata={'data ignore value': 0,
                                                   'description': 'COAL ' +
                                                   pycoal.version + ' mineral '
                                                                  'classified '
                                                                  'image.',
                                                   'map info':
                                                       image.metadata.get(
                                                        'map info')})

    if scores_file_name is not None:
        # save the scored image to a file
        spectral.io.envi.save_image(scores_file_name, scored,
                                    dtype=numpy.float64,
                                    metadata={'data ignore value': -50,
                                              'description': 'COAL ' +
                                                             pycoal.version
                                                             + ' mineral '
                                                               'scored '
                                                               'image.',
                                              'map info': image.metadata.get(
                                                  'map info')})


class MineralClassification:

    def __init__(self, algorithm=SAM_pytorch, **kwargs):
        """
        Construct a new ``MineralClassification`` object with a spectral
        library
        in ENVI format such as the `USGS Digital Spectral Library 06
        <https://speclab.cr.usgs.gov/spectral.lib06/>`_ or the `ASTER Spectral
        Library Version 2.0 <https://asterweb.jpl.nasa.gov/>`_ converted with
        ``pycoal.mineral.AsterConversion.convert()``.

        If provided, the optional class name parameter will initialize the
        classifier with a subset of the spectral library, otherwise the full
        spectral library will be used.

        Args:
            algorithm (function, optional): the classifier callback
            **kwargs: arguments that will be passed to the chosen classifier
        """

        # parse config file
        config = configparser.ConfigParser()
        
        try:
            with open('config.ini') as config_file:
                config.read_file(config_file)
        except IOError:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'config.ini')

        set_algo = None
        set_impl = None
        self.algorithm = algorithm
        
        # use the user's chosen classifier
        try:
            set_algo = config['processing']['algo']
        except KeyError:
            raise KeyError('Algorithm not set in config file')        
        
        # use the user's chosen implementation
        try:
            set_impl = config['processing']['impl']
        except KeyError:
            raise KeyError('Implementation not set in config file')
        
        
        if None not in (set_algo, set_impl):
            try:
                self.algorithm = globals()[set_algo + "_" + set_impl]
            except KeyError:
                raise KeyError('Algorithm or implementation set incorrectly in config file')
                
        # hold the remaining arguments that will be passed to self.algorithm
        self.args = kwargs

        logging.info(
            "Instantiated Mineral Classifier with following specification: "
            "-classifier function '%s'" % (self.algorithm.__name__,))

    def classify_image(self, image_file_name, classified_file_name):
        """
        Classify minerals in an AVIRIS image using chosen specified
        classification algorithm and save the results to a file.

        Args:
            image_file_name (str):      filename of the image to be classified
            classified_file_name (str): filename of the classified image

        Returns:
            None
        """
        start = time.time()
        logging.info("Starting Mineral Classification for image '%s', saving "
                     "classified image to '%s'" % (
                         image_file_name, classified_file_name))

        # run the classifier callback expanding self.args to fulfill the
        # specific args of the function
        self.algorithm(image_file_name, classified_file_name, **self.args)

        end = time.time()
        seconds_elapsed = end - start
        m, s = divmod(seconds_elapsed, 60)
        h, m = divmod(m, 60)
        logging.info(
            "Completed Mineral Classification. Time elapsed: '%d:%02d:%02d'"
            % (
                h, m, s))

    @staticmethod
    def filter_classes(classified_file_name):
        """
        Modify a classified image to remove unused classes.

        Args:
            classified_file_name (str): file of the classified image

        Returns:
            None
        """

        # open the image
        classified = spectral.open_image(classified_file_name)
        data = classified.asarray()
        M = classified.shape[0]
        N = classified.shape[1]

        # allocate a copy for reindexed pixels
        copy = numpy.zeros(shape=(M, N), dtype=numpy.uint16)

        # find classes actually present in the image
        classes = sorted(set(classified.asarray().flatten().tolist()))
        lookup = [classes.index(i) if i in classes else 0 for i in
                  range(int(classified.metadata.get('classes')))]

        # reindex each pixel
        for x in range(M):
            for y in range(N):
                copy[x, y] = lookup[data[x, y, 0]]

        # overwrite the file
        spectral.io.envi.save_classification(classified_file_name, copy,
                                             force=True,
                                             class_names=[
                                                 classified.metadata.get(
                                                     'class names')[i]
                                                 for i in classes],
                                             metadata=classified.metadata)

    @staticmethod
    def to_rgb(image_file_name, rgb_image_file_name, red=680.0, green=532.5,
               blue=472.5):
        """
        Generate a three-band RGB image from an AVIRIS image and save it to
        a file.

        Args:
            image_file_name (str):     filename of the source image
            rgb_image_file_name (str):  filename of the three-band RGB image
            red (float, optional):   wavelength in nanometers of the red band
            green (float, optional): wavelength in nanometers of the green band
            blue (float, optional):  wavelength in nanometers of the blue band

        Returns:
            None
        """

        # find the index of the first element in a list greater than the value
        start = time.time()
        logging.info(
            "Starting generation of three-band RGB image from input file: "
            "'%s' with following RGB values R: '%s', G: '%s', B: '%s'" % (
                image_file_name, red, green, blue))

        def index_of_greater_than(elements, value):
            for index, element in enumerate(elements):
                if element > value:
                    return index

        # open the image
        image = spectral.open_image(image_file_name)

        # load the list of wavelengths as floats
        wavelength_strings = image.metadata.get('wavelength')
        wavelength_floats = list(map(float, wavelength_strings))

        # find the index of the red, green, and blue bands
        red_index = index_of_greater_than(wavelength_floats, red)
        green_index = index_of_greater_than(wavelength_floats, green)
        blue_index = index_of_greater_than(wavelength_floats, blue)

        # read the red, green, and blue bands from the image
        red_band = image[:, :, red_index]
        green_band = image[:, :, green_index]
        blue_band = image[:, :, blue_index]

        # remove no data pixels
        for band in [red_band, green_band, blue_band]:
            band[numpy.where(numpy.logical_or(numpy.isclose(band[:,:,0], -0.005),band[:,:,0] == -50))] = 0

        # combine the red, green, and blue bands into a three-band RGB image
        rgb = numpy.concatenate([red_band, green_band, blue_band], axis=2)

        # update the metadata
        rgb_metadata = image.metadata
        rgb_metadata[
            'description'] = 'COAL ' + pycoal.version + ' three-band RGB ' \
                                                        'image.'
        rgb_metadata['data ignore value'] = 0
        if wavelength_strings:
            rgb_metadata['wavelength'] = [wavelength_strings[red_index],
                                          wavelength_strings[green_index],
                                          wavelength_strings[blue_index]]
        if image.metadata.get('correction factors'):
            rgb_metadata['correction factors'] = [
                image.metadata.get('correction factors')[red_index],
                image.metadata.get('correction factors')[green_index],
                image.metadata.get('correction factors')[blue_index]]
        if image.metadata.get('fwhm'):
            rgb_metadata['fwhm'] = [image.metadata.get('fwhm')[red_index],
                                    image.metadata.get('fwhm')[green_index],
                                    image.metadata.get('fwhm')[blue_index]]
        if image.metadata.get('bbl'):
            rgb_metadata['bbl'] = [image.metadata.get('bbl')[red_index],
                                   image.metadata.get('bbl')[green_index],
                                   image.metadata.get('bbl')[blue_index]]
        if image.metadata.get('smoothing factors'):
            rgb_metadata['smoothing factors'] = [
                image.metadata.get('smoothing factors')[red_index],
                image.metadata.get('smoothing factors')[green_index],
                image.metadata.get('smoothing factors')[blue_index]]

        # save the three-band RGB image to a file
        logging.info("Saving RGB image as '%s'" % rgb_image_file_name)
        spectral.envi.save_image(rgb_image_file_name, rgb,
                                 metadata=rgb_metadata)
        end = time.time()
        seconds_elapsed = end - start
        m, s = divmod(seconds_elapsed, 60)
        h, m = divmod(m, 60)
        logging.info(
            "Completed RGB image generation. Time elapsed: '%d:%02d:%02d'" % (
                h, m, s))

    @staticmethod
    def subset_spectral_library(spectral_library, class_names):

        # adapted from https://git.io/v9ThM

        """
        Create a copy of the spectral library containing only the named
        classes.

        Args:
            spectral_library (SpectralLibrary): ENVI spectral library
            class_names (str[]):                list of names of classes to
            include

        Returns:
            SpectralLibrary: subset of ENVI spectral library
        """

        # empty array for spectra
        spectra = numpy.empty(
            (len(class_names), len(spectral_library.bands.centers)))

        # empty list for names
        names = []

        # copy class spectra and names
        for new_index, class_name in enumerate(class_names):
            old_index = spectral_library.names.index(class_name)
            spectra[new_index] = spectral_library.spectra[old_index]
            names.append(class_name)

        # copy metadata
        metadata = {'wavelength units': spectral_library.metadata.get(
            'wavelength units'), 'spectra names': names,
            'wavelength': spectral_library.bands.centers}

        # return new spectral library
        return spectral.io.envi.SpectralLibrary(spectra, metadata, {})


class AsterConversion:

    def __init__(self):
        """
        This class provides a method for converting the `ASTER Spectral
        Library Version 2.0 <https://asterweb.jpl.nasa.gov/>`_ into ENVI
        format.
        """

    @classmethod
    def convert(cls, data_dir="", db_file="", hdr_file=""):
        """
        This class method generates an ENVI format spectral library file.
        ``data_dir`` is optional as long as ``db_file`` is provided. Note that
        generating an SQLite database takes upwards of 10 minutes and creating
        an ENVI format file takes up to 5 minutes. Note: This feature is still
        experimental.

        Args:
            data_dir (str, optional): path to directory containing ASCII
            data files
            db_file (str):            name of the SQLite file that either
            already exists if
                                      ``data_dir`` isn't provided, or will
                                      be generated if ``data_dir`` is provided
            hdr_file (str):           name of the ENVI spectral library to
                                      generate (without the ``.hdr`` or
                                      ``.sli`` extension)
        """
        if not hdr_file:
            raise ValueError(
                "Must provide path for generated ENVI header file.")

        elif not db_file:
            raise ValueError("Must provide path for sqlite file.")

        if data_dir:
            spectral.AsterDatabase.create(db_file, data_dir)

        aster_database = spectral.AsterDatabase(db_file)
        spectrum_ids = [x[0] for x in aster_database.query(
            'SELECT SampleID FROM Samples').fetchall()]
        band_min = 0.38315
        band_max = 2.5082
        band_num = 128
        band_info = spectral.BandInfo()
        band_info.centers = numpy.arange(band_min, band_max,
                                         (band_max - band_min) / band_num)
        band_info.band_unit = 'micrometer'
        library = aster_database.create_envi_spectral_library(spectrum_ids,
                                                              band_info)

        library.save(hdr_file)


class SpectalToAsterFileFormat:

    def __init__(self):
        """
            This class provides a method for converting `USGS Spectral
            Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ .txt files
            into ASTER Spectral
            Library Version 2.0 <https://asterweb.jpl.nasa.gov/> .txt files
            
            Args:
                none
            """

    @classmethod
    def convert(cls, library_filename=""):
        """
            This class method converts a `USGS Spectral Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ .txt file into
            an `ASTER Spectral Library Version 2.0
            <https://asterweb.jpl.nasa.gov/>`_ .spectrum.txt file
            ASTER Library Version 2.0 Spectral Library files are in
            .spectrum.txt file format
            
            Spectral Library Version 7 can be downloaded `here
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_
            
            Args:
            library_filename (str): path to Spectral File you wish to convert
            """
        if not library_filename:
            raise ValueError("Must provide path for Spectral File.")

        line_count = 1
        with open(library_filename, 'r') as input_file:
            for line_count, _ in enumerate(input_file):
                pass

        input_file = open(library_filename, 'r')
        # Read Name of Spectra on first line of the file
        spectra_line = input_file.readline()
        spectra_name = spectra_line[23:]
        k = 0
        # Loop through file and store all wavelength values for the given
        # Spectra
        spectra_values_file = open('SpectraValues.txt', 'w')
        spectra_wave_length = 0
        while (k < line_count):
            spectra_wave_length = float(input_file.readline()) * 100
            spectra_wave_length = spectra_wave_length / 1000
            spectra_wave_length = float("{0:.5f}".format(spectra_wave_length))
            spectra_y_value = spectra_wave_length * 10
            line = str(spectra_wave_length) + '  ' + str(spectra_y_value)
            spectra_values_file.write(line)
            spectra_values_file.write('\n')
            k = k + 1
        # Write new file in the form of an ASTER .spectrum.txt file while
        # using stored
        # Spectra Name and stored Spectra Wavelength values`
        input_file = open(library_filename, 'w')
        input_file.write('Name:')
        input_file.write(spectra_name)
        input_file.write('Type:\n')
        input_file.write('Class:\n')
        input_file.write('Subclass:\n')
        input_file.write('Particle Size:  Unknown\n')
        input_file.write('Sample No.:  0000000000\n')
        input_file.write('Owner:\n')
        input_file.write('Wavelength Range:  ALL\n')
        input_file.write(
            'Origin: Spectra obtained from the Noncoventional Exploitation '
            'Factors\n')
        input_file.write(
            'Data System of the National Photographic Interpretation '
            'Center.\n')
        input_file.write(
            'Description:  Gray and black construction asphalt.  The sample '
            'was\n')
        input_file.write(
            'soiled and weathered, with some limestone and quartz aggregate\n')
        input_file.write('showing.\n')
        input_file.write('\n')
        input_file.write('\n')
        input_file.write('\n')
        input_file.write('Measurement:  Unknown\n')
        input_file.write('First Column:  X\n')
        input_file.write('Second Column: Y\n')
        input_file.write('X Units:  Wavelength (micrometers)\n')
        input_file.write('Y Units:  Reflectance (percent)\n')
        input_file.write('First X Value:\n')
        input_file.write('Last X Value:\n')
        input_file.write('Number of X Values:\n')
        input_file.write('Additional Information:\n')
        input_file.write('\n')
        j = 0
        spectra_values_file.close()
        # Read in values saved in SpectraValues.txt and output them to the
        # library_filename
        spectra_values_file = open('SpectraValues.txt', 'r')
        while (j < line_count):
            spectra_wave_length = spectra_values_file.readline()
            input_file.write(spectra_wave_length)
            j = j + 1
        # Close all open files
        input_file.close()
        spectra_values_file.close()
        # Rename library_filename to match ASTER .spectrum.txt file format
        os.rename(library_filename, library_filename + '.spectrum.txt')
        # Remove temporary file for storing wavelength data
        os.remove('SpectraValues.txt')


class FullSpectralLibrary7Convert:
    def __init__(self):
        """
            This class method converts the entire `USGS Spectral Library
            Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ library into
            its convolved envi format
            
            Args:
            none
            """

    @classmethod
    def convert(cls, library_filename=""):
        """
            This class method converts the entire `USGS Spectral Library
            Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ library into
            its convolved envi format
            
            Spectral Library Version 7 can be downloaded `here
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_
            
            Args:
            library_filename (str): path to USGS Spectral Library Version 7
            directory
            """
        if not library_filename:
            raise ValueError(
                "Must provide path for USGS Spectral Library Version 7.")

        # This will take all the necessary .txt files for spectra in USGS
        # Spectral Library Version 7 and put them in a new directory called
        # "usgs_splib07_modified" in the examples directory
        directory = 'usgs_splib07_modified'
        if not os.path.exists(directory):
            os.makedirs(directory)

        for root, dir, files in os.walk(library_filename + "/ASCIIdata"):
            dir[:] = [d for d in dir]
            for items in fnmatch.filter(files, "*.txt"):
                if "Bandpass" not in items:
                    if "errorbars" not in items:
                        if "Wave" not in items:
                            if "SpectraValues" not in items:
                                shutil.copy2(os.path.join(root, items),
                                             directory)

        # This will take the .txt files for Spectra in USGS Spectral Version
        # 7 and
        # convert their format to match that of ASTER .spectrum.txt files
        # for spectra
        # create a new mineral aster conversion instance
        spectral_aster = SpectalToAsterFileFormat()
        # List to check for duplicates
        spectra_list = []
        # Convert all files
        files = os.listdir(directory + '/')
        for _, file in enumerate(files):
            name = directory + '/' + file
            # Get name
            with open(name, 'r') as input_file:
                spectra_line = input_file.readline()
            spectra_cut = spectra_line[23:]
            spectra_name = spectra_cut[:-14]
            # Remove first and last char in case extra spaces are added
            spectra_first_space = spectra_name[1:]
            spectra_last_space = spectra_first_space[:-1]

            # Check if Spectra is unique
            set_spectra = set(spectra_list)
            if not any(spectra_name in s for s in set_spectra):
                if not any(spectra_last_space in a for a in set_spectra):
                    spectral_aster.convert(name)
                    spectra_list.append(spectra_name)

        set_spectra = set(spectra_list)
        print(set_spectra)

        # This will generate three files s07AV95a_envi.hdr,
        # s07AV95a_envi.hdr.sli,splib.db and dataSplib07.db
        # For a library in `ASTER Spectral Library Version 2.0
        # <https://asterweb.jpl.nasa.gov/>`_ format
        data_dir = "dataSplib07.db"
        # Avoid overwrite during nosetests of full .hdr and .sli files with
        # sample .hdr and .sli
        if (os.path.isfile('s07_AV95_envi.hdr')):
            header_name = "s07_AV95_envi_sample"
        else:
            header_name = "s07_AV95_envi"
        # create a new mineral aster conversion instance
        spectral_envi = AsterConversion()
        # Generate .sli and .hdr
        spectral_envi.convert(directory, data_dir, header_name)

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

import glob
from subprocess import call
import spectral
import numpy
from os.path import abspath, dirname, basename, splitext
import platform
import pycoal
import logging
import time


class EnvironmentalCorrelation:

    def __init__(self):
        """
        Construct a new ``EnvironmentalCorrelation`` object.
        """
        logging.info(
            "Instantiated Environmental Correlation module with following "
            "specification: ")

    @staticmethod
    def intersect_proximity(mining_filename, vector_filename, proximity,
                            correlated_filename):
        """
        Generate an environmental correlation image containing pixels from the
        mining classified image detected within a given distance of features
        within a vector layer.

        Args:
            mining_filename (str):     filename of the mining classified image
            vector_filename (str):     filename of vector layer
            proximity (float):         distance in meters
            correlated_filename (str): filename of the correlated image
        """
        start = time.time()
        logging.info(
            "Starting Environmental Correlation for mining image '%s', "
            "with vector layer '%s' and proximity distance of '%s' meters.",
            mining_filename, vector_filename, proximity)
        # get path and file names
        output_directory = dirname(abspath(correlated_filename))
        mining_name = splitext(basename(abspath(mining_filename)))[0]
        vector_name = splitext(basename(abspath(vector_filename)))[0]

        # rasterize the vector features to the same dimensions as the mining
        # image
        feature_header_name = output_directory + '/' + mining_name + '_' +\
            vector_name + '.hdr'
        EnvironmentalCorrelation.create_empty_copy(mining_filename,
                                                   feature_header_name)
        feature_image_name = feature_header_name[:-4] + '.img'
        EnvironmentalCorrelation.rasterize(vector_filename, feature_image_name)

        # generate a proximity map from the features
        proximity_header_name = output_directory + '/' + mining_name + '_' +\
            vector_name + '_proximity.hdr'
        proximity_image_name = proximity_header_name[:-4] + '.img'
        EnvironmentalCorrelation.proximity(feature_image_name,
                                           proximity_image_name)

        # load mining and proximity images and initialize environmental
        # correlation array
        mining_image = spectral.open_image(mining_filename)
        proximity_image = spectral.open_image(proximity_header_name)
        correlated_image = numpy.zeros(shape=mining_image.shape,
                                       dtype=numpy.uint16)

        # get average pixel size
        if mining_image.metadata.get('map info')[10][-6:].lower() == 'meters':
            x_pixel_size = float(mining_image.metadata.get('map info')[5])
            y_pixel_size = float(mining_image.metadata.get('map info')[6])
            pixel_size = (x_pixel_size + y_pixel_size) / 2
        else:
            raise ValueError('Mining image units not in meters.')

        # intersect features within proximity
        for x in range(mining_image.shape[0]):
            for y in range(mining_image.shape[1]):
                if mining_image[x, y, 0] == 1 \
                        and proximity_image[x, y, 0] * pixel_size <= proximity:
                    correlated_image[x, y, 0] = mining_image[x, y, 0]

        # save the environmental correlation image
        spectral.io.envi.save_classification(correlated_filename,
                                             correlated_image,
                                             class_names=mining_image.
                                             metadata.get('class names'),
                                             metadata={'data ignore value': 0,
                                                       'description': 'COAL ' +
                                                       pycoal.version + ' '
                                                       'environmental '
                                                       'correlation image.',
                                                       'map info':
                                                           mining_image.
                                                           metadata.get(
                                                               'map info')})
        logging.info(
            "Successfully saved Environmental Correlation image to '%s'.",
            correlated_filename)
        end = time.time()
        seconds_elapsed = end - start
        m, s = divmod(seconds_elapsed, 60)
        h, m = divmod(m, 60)
        logging.info(
            "Completed Environmental Correlation. Time elapsed: "
            "'%d:%02d:%02d'", h, m, s)

    @staticmethod
    def create_empty_copy(source_filename, destination_filename):
        """
        Create an empty copy of a COAL classified image with the same size.

        Args:
            source_filename (str):      filename of the source image
            destination_filename (str): filename of the destination image
        """
        logging.info(
            "Creating an empty copy of classified image '%s' with the same "
            "size. Saving to '%s'", source_filename, destination_filename)
        # open the source image
        source = spectral.open_image(source_filename)

        # create an empty array of the same dimensions
        destination = numpy.zeros(shape=source.shape, dtype=numpy.uint16)

        # save it with source metadata
        spectral.io.envi.save_classification(destination_filename, destination,
                                             class_names=['No data', 'Data'],
                                             metadata={'data ignore value': 0,
                                                       'map info':
                                                           source.metadata.get(
                                                               'map info')})

    @staticmethod
    def rasterize(vector_filename, feature_filename):
        """
        Burn features from a vector image onto a raster image.

        Args:
            vector_filename (str):  filename of the vector image
            feature_filename (str): filename of the raster image
        """
        logging.info(
            "Burning features from vector file: '%s' to raster file: '%s'",
            vector_filename, feature_filename)
        # assume the layer has the same name as the image
        layer_name = splitext(basename(vector_filename))[0]

        # convert vector features into nonzero pixels of the output file
        returncode = call(
            ['gdal_rasterize', '-burn', '1', '-l', layer_name, vector_filename,
             feature_filename])

        # detect errors
        if returncode != 0:
            raise RuntimeError('Could not rasterize vector.')

    @staticmethod
    def proximity(feature_filename, proximity_filename):
        """
        Generate a proximity map from the features.
        N.B. it is essential to have 
        `GDAL's gdal_proximity.py <http://www.gdal.org/gdal_proximity.html>`_
        available somewhere on the path. If running Mac OSX, this function will
        scan ``/Library/Frameworks/GDAL.framework/.../gdal_proximity.py`` (
        which is where
        the binary package installer installs it to) to locate the file.
        Alternatively, ensure that gdal_proximity.py can be called in the
        current environment.

        Args:
            feature_filename (str): filename of the feature image
            proximity_filename (str): filename of the proximity image
        """
        logging.info(
            "Generating a proximity map from features of '%s', writing them "
            "to '%s'", feature_filename, proximity_filename)

        # search for gdal_proximity on macOS
        gdal_proximity = None
        if platform.system() == 'Darwin':
            for file in glob.glob(
                    "/Library/Frameworks/GDAL.framework/**/gdal_proximity.py"):
                if file is not None:
                    logging.info("Located gdal_proximity.py at %s", file)
                    gdal_proximity = file
                else:
                    logging.info(
                        "Unable to locate gdal_proximity.py via GDAL binary "
                        "install.")

        # generate an ENVI proximity map with georeferenced units
        returncode = call([('gdal_proximity.py' if gdal_proximity is None
                            else gdal_proximity), feature_filename,
                           proximity_filename, '-of',
                           'envi'])

        # detect errors
        if returncode != 0:
            raise RuntimeError('Could not generate proximity map.')

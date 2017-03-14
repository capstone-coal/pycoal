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

import numpy
import spectral

class MineralClassification:

    def __init__(self, libraryFilename):
        """
        Construct a new MineralClassification object with the USGS Digital
        Spectral Library 06.

        Args:
            libraryFilename (str):    filename of the spectral library
        """
        self.library = spectral.open_image(libraryFilename)

    def classifyImage(imageFilename, classifiedFilename):
        """
        Classify minerals in an AVIRIS image using spectral angle mapper
        classification and save the results to a file.

        Args:
            imageFilename (str):      filename of the image to be classified
            classifiedFilename (str): filename of the classified image

        Returns:
            None
        """

        # open the image
        image = spectral.open_image(imageFilename)
        data = image.asarray()
        M = image.shape[0]
        N = image.shape[1]

        # define a resampler
        # TODO detect and scale units
        # TODO band resampler should do this
        resample = spectral.BandResampler([x/1000 for x in image.bands.centers],
                                      self.library.bands.centers)

        # allocate a zero-initialized MxN array for the classified image
        classified = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # for each pixel in the image
        for x in xrange(M):

            for y in xrange(N):

                # read the pixel from the file
                pixel = data[x,y]

                # if it is not a no data pixel
                if not numpy.isclose(pixel[0], -0.005):

                    # resample the pixel ignoring NaNs from target bands that don't overlap
                    # TODO fix spectral library so that bands are in order
                    resampledPixel = numpy.nan_to_num(resample(pixel))

                    # calculate spectral angles
                    angles = spectral.spectral_angles(resampledPixel[numpy.newaxis,
                                                                     numpy.newaxis,
                                                                     ...],
                                                      self.library.spectra)

                    # get classification
                    classified[x,y] = numpy.argmin(angles) + 1

        # save the classified image to a file
        spectral.io.envi.save_classification(classifiedFilename,
                                             classified,
                                             class_names=['No data']+self.library.names,
                                             metadata={
                                                 'data ignore value': 0,
                                                 'description': 'Mineral classified image.',
                                                 'map info': image.metadata.get('map info')
                                             })

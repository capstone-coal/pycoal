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
import pycoal

class MineralClassification:

    def __init__(self, libraryFilename):
        """
        Construct a new MineralClassification object with the `USGS Digital
        Spectral Library 06 <https://speclab.cr.usgs.gov/spectral.lib06/>`_
        in ENVI format.

        Args:
            libraryFilename (str):    filename of the spectral library
        """
        self.library = spectral.open_image(libraryFilename)

    def classifyImage(self, imageFilename, classifiedFilename):
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
        for x in range(M):

            for y in range(N):

                # read the pixel from the file
                pixel = data[x,y]

                # if it is not a no data pixel
                if not numpy.isclose(pixel[0], -0.005) and not pixel[0]==-50:

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
                                                 'description': 'PyCOAL '+pycoal.version+' mineral classified image.',
                                                 'map info': image.metadata.get('map info')
                                             })

        # remove unused classes from the image
        pycoal.mineral.MineralClassification.filterClasses(classifiedFilename)

    @staticmethod
    def filterClasses(classifiedFilename):
        """
        Modify a classified image to remove unused classes.

        Args:
            classifiedFilename (str): file of the classified image

        Returns:
            None
        """

        # open the image
        classified = spectral.open_image(classifiedFilename)
        data = classified.asarray()
        M = classified.shape[0]
        N = classified.shape[1]

        # allocate a copy for reindexed pixels
        copy = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # find classes actually present in the image
        classes = sorted(set(classified.asarray().flatten().tolist()))
        lookup = [classes.index(i) if i in classes else 0 for i in range(int(classified.metadata.get('classes')))]

        # reindex each pixel
        for x in range(M):
            for y in range(N):
                copy[x,y] = lookup[data[x,y,0]]

        # overwrite the file
        spectral.io.envi.save_classification(classifiedFilename,
                                             copy,
                                             force=True,
                                             class_names=[classified.metadata.get('class names')[i] for i in classes],
                                             metadata=classified.metadata)

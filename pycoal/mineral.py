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

    @staticmethod
    def toRGB(imageFilename, rgbImageFilename, red=680.0, green=532.5, blue=472.5):
        """
        Generate a three-band RGB image from an AVIRIS image and save it to a file.

        Args:
            imageFilename (str):     filename of the source image
            rgbImageFilename (str):  filename of the three-band RGB image
            red (float, optional):   wavelength in nanometers of the red band
            green (float, optional): wavelength in nanometers of the green band
            blue (float, optional):  wavelength in nanometers of the blue band

        Returns:
            None
        """

        # find the index of the first element in a list greater than the value
        def indexOfGreaterThan(elements, value):
            for index,element in enumerate(elements):
                if element > value:
                    return index

        # open the image
        image = spectral.open_image(imageFilename)

        # load the list of wavelengths as floats
        wavelengthStrings = image.metadata.get('wavelength')
        wavelengthFloats = map(float, wavelengthStrings)

        # find the index of the red, green, and blue bands
        redIndex = indexOfGreaterThan(wavelengthFloats, red)
        greenIndex = indexOfGreaterThan(wavelengthFloats, green)
        blueIndex = indexOfGreaterThan(wavelengthFloats, blue)

        # read the red, green, and blue bands from the image
        redBand = image[:,:,redIndex]
        greenBand = image[:,:,greenIndex]
        blueBand = image[:,:,blueIndex]

        # combine the red, green, and blue bands into a three-band RGB image
        rgb = numpy.concatenate([redBand,greenBand,blueBand], axis=2)

        # update the metadata
        rgbMetadata = image.metadata
        rgbMetadata['description'] = 'PyCOAL '+pycoal.version+' three-band RGB image.'
        rgbMetadata['wavelength'] = [wavelengthStrings[redIndex],
                                     wavelengthStrings[greenIndex],
                                     wavelengthStrings[blueIndex]]
        rgbMetadata['correction factors'] = [image.metadata.get('correction factors')[redIndex],
                                             image.metadata.get('correction factors')[greenIndex],
                                             image.metadata.get('correction factors')[blueIndex]]
        rgbMetadata['fwhm'] = [image.metadata.get('fwhm')[redIndex],
                               image.metadata.get('fwhm')[greenIndex],
                               image.metadata.get('fwhm')[blueIndex]]
        rgbMetadata['bbl'] = [image.metadata.get('bbl')[redIndex],
                              image.metadata.get('bbl')[greenIndex],
                              image.metadata.get('bbl')[blueIndex]]
        rgbMetadata['smoothing factors'] = [image.metadata.get('smoothing factors')[redIndex],
                                            image.metadata.get('smoothing factors')[greenIndex],
                                            image.metadata.get('smoothing factors')[blueIndex]]

        # save the three-band RGB image to a file
        spectral.envi.save_image(rgbImageFilename, rgb, metadata=rgbMetadata)

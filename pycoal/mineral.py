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

def classifyImage(imageFilename, libraryFilename, classifiedFilename):
    """
    Classify minerals in an AVIRIS image using spectral angle mapper classification with a spectral library and save the results to a file.

    Args:
       imageFilename (str):      filename of the image to be classified
       libraryFilename (str):    filename of the spectral library
       classifiedFilename (str): filename of the classified image

    Returns:
        None
    """

    # open the image
    image = spectral.open_image(imageFilename)
    data = image.asarray()
    M = image.shape[0]
    N = image.shape[1]

    # open the library
    library = spectral.open_image(libraryFilename)

    # define a resampler
    # TODO detect and scale units
    # TODO band resampler should do this
    resample = spectral.BandResampler([x/1000 for x in image.bands.centers], library.bands.centers)

    # allocate an MxN array for the classified image
    classified = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

    # for each pixel in the image
    for x in xrange(M):

        for y in xrange(N):

            # read the pixel from the file
            pixel = data[x,y]

            # if it is a no data pixel
            if pixel[0] < 0:

                # give it a negative class id
                classified[x,y] = -1;

            # otherwise
            else:

                # resample the pixel ignoring NaNs from target bands that don't overlap
                # TODO fix spectral library so that bands are in order
                resampledPixel = numpy.nan_to_num(resample(pixel))

                # calculate spectral angles
                angles = spectral.spectral_angles(resampledPixel[numpy.newaxis,numpy.newaxis,...], library.spectra)

                # get classification
                classified[x,y] = numpy.argmin(angles)

    # save the classified image to a file
    spectral.io.envi.save_classification(classifiedFilename, classified, class_names=library.names)

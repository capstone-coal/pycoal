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

import spectral
import pycoal
import numpy

class MiningClassification:

    def __init__(self, classNames=None):
        """
        Construct a new MiningClassification object given a list of spectral
        class names corresponding to mines or other features.

        Args:
            classes (str[]): list of class names to identify.
        """

        self.classNames = classNames

    def classifyImage(self, imageFilename, classifiedFilename):

        """
        Classify mines or other features in a Pycoal classified image by copying
        relevant pixels and discarding the rest in a new file.

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

        # allocate a zero-initialized MxN array for the classified image
        classified = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # get class numbers from names
        classNums = [image.metadata.get('class names').index(className) for className in self.classNames]

        # for each pixel in the image
        for y in xrange(N):

            for x in xrange(M):

                pixel = data[x,y]

                if pixel[0] in classNums:

                    classified[x,y] = 1 + classNums.index(pixel[0])

        # save the classified image to a file
        spectral.io.envi.save_classification(classifiedFilename,
                                             classified,
                                             class_names=['No data']+self.classNames,
                                             metadata={
                                                 'data ignore value': 0,
                                                 'description': 'PyCOAL '+pycoal.version+' mining classified image.',
                                                 'map info': image.metadata.get('map info')
                                             })

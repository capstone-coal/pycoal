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
import numpy

class MineralClassification:
    def __init__(self):
        # define wavelength range in micrometers
        self.wavelength_min = 0.38315
        self.wavelength_max = 2.5082

        # define number of layers in normalized pixel
        self.num_layers = 128

    def normalize(self, image, wavelengthList=None):
        """
        Return a copy of an MxNxB image (or 1x1xB pixel) with constrained wavelength range and normalized spectra.
        Args:
           image (numpy.ndarray): the image or pixel to normalize
           wavelengthList (list) [default None]: the list of wavelengths for the pixel
        Returns:
           normalizedImage (numpy.ndarray): the normalized image or pixel
        """

        # constrain wavelength range
        if wavelengthList is None:
            wavelengthList = map(float, image.metadata.get('wavelength'))

        # get the indices of the minimum and maximum element
        i = self.__indexOfGreaterThan(wavelengthList, self.wavelength_min)
        j = self.__indexOfGreaterThan(wavelengthList, self.wavelength_max)

        # constrain wavelength range
        # slice the array from MxNxB to MxNx(j-i) for indices i,j
        image = image[:,:,i:j]

        # normalize spectra
        principalComponents = spectral.algorithms.principal_components(image)
        reduced = principalComponents.reduce(num=self.num_layers)
        normalizedImage = reduced.transform(image)

        # return normalized image
        return normalizedImage

    @staticmethod
    def __indexOfGreaterThan(elements, value):
        """
        Return the index of the first element greater than the value.
        Args:
           elements (list): list of elements
           value (float): the value to compare
        Returns:
           index (int): the index of the first element greater than the value
        """

        for index,element in enumerate(elements):
            if element > value:
                break
        return index

    def classifyPixel(self, pixel, classifier, wavelengthList):
        """
        Return the class id of an AVIRIS pixel classified using a trained classifier.
        Args:
            pixel (???): the pixel to be classified
           classifier (PerceptronClassifier): the classifier
           wavelengthList (list): the list of wavelengths for the pixel
        Returns:
            (int) Class ID of pixel
        """
        # classify normalized pixel and return class id
        return classifier.classify_spectrum(self.normalize(pixel, wavelengthList))

    def classifyImage(self, imageFilename, classifier, classifiedImageFilename):
        """
        Classify an AVIRIS image using a trained classifier and save the results to a file.
        Args:
           imageFilename (str): the image to be classified
           classifier (PerceptronClassifier): the classifier
           classifiedImageFilename (str): the file which to save the classified image
        Returns:
            None
        """

        # open the image
        image = spectral.io.aviris.open(imageFilename)

        # get wavelength list
        wavelengthList = map(float, image.metadata.get('wavelength'))

        # change units from nanometers to micrometers if applicable
        if image.metadata.get('wavelength units') == u'Nanometers':
            image.metadata['wavelength'] = [x / 1000 for x in image.metadata.get('wavelength')]
            image.metadata['wavelength units'] = u'Micrometers'

        # allocate an MxN array for the classified image
        classifiedImage = numpy.ndarray((image.shape[0] * image.shape[1],))

        # the index of the where to store the next classified pixel
        imageIndex = 0

        # TODO conditionally load entire image ?
        # TODO conditionally load subimage (row) ?

        # get an iterator over pixels in the image
        pixelIterator = spectral.algorithms.ImageIterator(image)

        # for each pixel in the image
        for pixel in pixelIterator:

            # TODO convert units ?
            # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

            # define a linear transformation to scale the pixel if necessary
            # the scalars would presumably be read from metadata
            #transform = spectral.transforms.LinearTransform(???)

            # transform it
            #transformedPixel = transform(pixel)

            # classify and store it in the classified image
            classifiedImage[imageIndex] = self.classifyPixel(pixel, classifier, wavelengthList)

            imageIndex += 1
        # save the classified image to a file
        spectral.io.envi.save_classification(classifiedImageFilename, classifiedImage)

    def classifyImages(self, imageFilenames, classifier, classifiedImageFilenames):
        """
        Classify a set of AVIRIS images using a trained classifier and save the results to files.
        Args:
           imageFilenames (str): the images to be classified
           classifier (PerceptronClassifier): the classifier
           classifiedImageFilenames (str): the files which to save the classified images
        Returns:
            None
        """

        # for each image in a set of images
        for imageFilename,classifiedImageFilename in zip(imageFilenames,classifiedImageFilenames):

            # classify the image and save it to a file
            self.classifyImage(imageFilename, classifier, classifiedImageFilename)


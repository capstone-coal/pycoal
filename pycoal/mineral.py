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
import pickle
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
        principalComponents.reduce(self.num_layers)
        normalizedImage = principalComponents.transform(image)

        # return normalized image
        return normalizedImage

    def __indexOfGreaterThan(self, elements, value):
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

    def trainClassifier(self, libraryFileName, classifierType='gaussian'):
        """
        This takes the file name of the library to be used in the training and returns a
        classifier
        Args:
           libraryFileName (str): the name of the training library
           classifierType (str) [default 'gaussian']: the type of classifier.
                                                      Currently, can be one of:
                                                      perceptron, gaussian, or
                                                      mahalanobisdistance.
        Returns:
           classifier (PerceptronClassifier, GaussianClassifier,
                       or MahalanobisDistanceClassifier): trained classifier
        """

        # open the digital spectral library
        # we may need to load it as an image instead
        library = spectral.io.envi.open(libraryFileName)

        # get dimensions of library to create mask for training class
        dimensions = library.spectra.shape

        # initialize the type of classifier
        if classifierType == 'perceptron':
            # try out using the neural net structure used in the following
            # paper: http://www.aaai.org/Papers/FLAIRS/1999/FLAIRS99-057.pdf
            nn_structure = [9, 35, 60]
            classifier = spectral.classifiers.PerceptronClassifier(nn_structure)
        elif classifierType == 'gaussian':
            classifier = spectral.classifiers.GaussianClassifier()
        elif classifierType == 'mahalanobisdistance':
            classifier = spectral.classifiers.MahalanobisDistanceClassifier()
        else:
            raise ValueError('Invalid classifier type provided.')

        # create mask of distinct values.
        mask = numpy.ndarray(shape=dimensions)

        # is there a more concise way of doing this?
        value = 1
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                mask[i][j] = value
                value += 1

        # generate training data
        trainingData = spectral.algorithms.create_training_classes(self.normalize(library), mask)

        # initialize and train a neural network using the training data
        classifier.train(trainingData)

        # return trained classifier
        return classifier

    def saveClassifier(self, classifier, classifierFilename):
        """
        This saves a classifier to a file for reuse.
        Args:
           classifier (PerceptronClassifier): the classifier to write
           classifierFilename (str): the file which to write the classifier
        Returns:
            None
        """

        with open(classifierFilename,"wb") as f:
            pickle.dump(classifier, f)

    def readClassifier(self, classifierFilename):
        """
        This reads a classifier from a file.
        Args:
           classifierFilename (str): the file from which to load the classifier
        Returns:
            ??? not sure about how to express this
        """

        with open(classifierFilename, "rb") as f:
            return pickle.load(f)

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


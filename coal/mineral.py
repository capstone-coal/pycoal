#!/usr/bin/python

import spectral
import pickle

# define number of layers in normalized pixel
NUMBER_OF_LAYERS = 128

# define wavelength range
WAVELENGTH_MIN = ???
WAVELENGTH_MAX = ???

def normalize(image):

    """
    Return a copy of an MxNxB image (or 1x1xB pixel) with constrained wavelength range and normalized spectra.
    """

    # TODO constrain wavelength range
    # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

    # normalize spectra
    principalComponents = spectral.algorithms.algorithms.principal_components(image)
    principalComponents.reduce(NUMBER_OF_LAYERS, ???)
    normalizedImage = principalComponents.transform(image)

    # return normalized image
    return normalizedImage

def trainClassifier(libraryFileName):

    """
    Return a trained classifier given the path to the USGS Digital Spectral Library 06 in AVIRIS format.
    """

    # open the digital spectral library
    # we may need to load it as an image instead
    library = spectral.io.envi.open(libraryFilename)

    # TODO convert units ?
    # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

    # generate training data
    trainingData = ???(normalize(???(library)))

    # initialize and train a neural network using the training data
    classifier = spectral.algorithms.classifiers.PerceptronClassifier(???)
    classifier.train(trainingData, ???)

    # TODO close file ?

    # return trained classifier
    return classifier

def saveClassifier(classifier, classifierFilename):

    """
    Save a classifier to a file.
    """

    # TODO close file ?

    pickle.dump(classifier, open(classifierFilename,"wb"))

def readClassifier(classifierFilename):

    """
    Read a classifier from a file.
    """

    # TODO close file ?

    return pickle.load(open(classifierFilename,"rb"))

def classifyPixel(pixel, classifier):

    """
    Return the class id of an AVIRIS pixel classified using a trained classifier.
    """

    # classify normalized pixel and return class id
    return classifier.classify_spectrum(normalize(pixel))

def classifyImage(imageFilename, classifier, classifiedImageFilename):

    """
    Classify an AVIRIS image using a trained classifier and save the results to a file.
    """

    # open the image
    image = spectral.io.aviris.open_image(imageFilename)

    # allocate an MxN array for the classified image
    classifiedImage = numpy.ndarray(???)

    # TODO conditionally load entire image ?
    # TODO conditionally load subimage (row) ?

    # get an iterator over pixels in the image
    pixelIterator = spectral.algorithms.algorithms.ImageIterator(image)

    # for each pixel in the image
    for pixel in pixelIterator:

        # TODO convert units ?
        # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

        # define a linear transformation to scale the pixel if necessary
        # the scalars would presumably be read from metadata
        transform = spectral.algorithms.transforms.LinearTransform(???)

        # transform it
        transformedPixel = transform(pixel)

        # classify and store it in the classified image
        classifiedImage[???] = classifyPixel(transformedPixel, classifier)

    # save the classified image to a file
    spectral.io.envi.save_classification(classifiedImageFilename, classifiedImage, ???)

    # TODO close files ?

def classifyImages(imageFilenames, classifier, classifiedImageFilenames):

    """
    Classify a set of AVIRIS images using a trained classifier and save the results to files.
    """

    # for each image in a set of images
    for imageFilename,classifiedImageFilename in zip(imageFilenames,classifiedImageFilenames):

        # classify the image and save it to a file
        classifyImage(imageFilename, classifier, classifiedImageFilename)

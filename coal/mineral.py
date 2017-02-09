#!/usr/bin/env python

import spectral
import pickle

# define number of layers in normalized pixel
NUMBER_OF_LAYERS = 128

# define wavelength range in nanometers
WAVELENGTH_MIN = 383.150
WAVELENGTH_MAX = 2508.200

def normalize(image):
    """
    This takes the file name of the library to be used in the training and returns a
    classifier
    Args:
       image (str): the image to normalize
    Returns:
       normalizedImage (LinearTransform): LinearTransform object?
    """

    # TODO constrain wavelength range
    # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

    # normalize spectra
    #
    principalComponents = spectral.algorithms.algorithms.principal_components(image)
    principalComponents.reduce(NUMBER_OF_LAYERS, ???)
    normalizedImage = principalComponents.transform(image)

    # return normalized image
    return normalizedImage

def trainClassifier(libraryFileName):
    """
    This takes the file name of the library to be used in the training and returns a
    classifier
    Args:
       libraryFileName (str): the name of the training library
    Returns:
       classifier (PerceptronClassifier): trained classifier
    """

    # open the digital spectral library
    # we may need to load it as an image instead
    library = spectral.io.envi.open(libraryFilename)

    # TODO convert units ?
    # see https://groups.google.com/d/msg/coal-capstone/6oordALy0dA/a_6VIuWbBAAJ

    # generate training data
    trainingData = ???(normalize(???(library)))

    # initialize and train a neural network using the training data
    classifier = spectral.classifiers.PerceptronClassifier(???)
    classifier.train(trainingData, ???)

    # return trained classifier
    return classifier

def saveClassifier(classifier, classifierFilename):
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

def readClassifier(classifierFilename):
    """
    This reads a classifier from a file.
    Args:
       classifierFilename (str): the file from which to load the classifier
    Returns:
        ??? not sure about how to express this
    """

    with open(classifierFilename, "rb") as f:
        return pickle.load(f)

def classifyPixel(pixel, classifier):
    """
    Return the class id of an AVIRIS pixel classified using a trained classifier.
    Args:
        pixel (???): the pixel to be classified
       classifier (PerceptronClassifier): the classifier
    Returns:
        Class ID of pixel
    """
    # classify normalized pixel and return class id
    return classifier.classify_spectrum(normalize(pixel))

def classifyImage(imageFilename, classifier, classifiedImageFilename):
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

def classifyImages(imageFilenames, classifier, classifiedImageFilenames):
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
        classifyImage(imageFilename, classifier, classifiedImageFilename)


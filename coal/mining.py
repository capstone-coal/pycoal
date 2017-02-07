#!/usr/bin/env python

# TODO shrink not overlap ? pixel subset ?

# TODO use spectral or gdal/orfeo for dataset manipulation and machine learning ?

import coal

def generateTrainingData(miningFilename, mineralFilename, trainingFilename):

    """
    Generate training data for mining classification by comparing a GIS mining map with the region surrounding each pixel in a mineral-classified image and writing the result to a file.
    """

    # define function to select the mining layer
    def miningLayer(miningDataset):

        return ???

    # define raster function to classify mineral regions with known mines
    def pixelNeighbors(miningDataset, mineralDataset, resultDataset):

        # TODO represent as dataset or array ?

        # for each pixel in the mining and mineral-classified datasets
        for ???:

            # get the region surrounding the mineral-classified pixel as a multiband pixel
            mineralRegion = getRegionAsMultibandPixel(mineralDataset, x, y)

            # get the mining pixel
            miningPixel = ???

            # classify the region with the mining pixel
            ???

    # apply the correlation and save the result
    coal.gis.combine(pixelNeighbors, miningLayer, miningFilename, mineralFilename, trainingFilename)

def trainMiningClassifier(miningFilename, mineralFilename):

    """
    Return a trained mining classifier given a mineral classified image and a GIS mining map.
    """

    # generate training data in a temporary file
    trainingFilename = ???
    generateTrainingData(mineralFilename, miningFilename, trainingFilename)

    # load training data
    trainingData = ???(trainingFilename)

    # initialize and train a neural network using the training data
    ???(trainingData)

    # TODO delete temporary file ?

    # return trained mining clasifier
    return classifier

def classifyRegion(mineralRegion, miningClassifier):

    """
    """

    return ???

def classifyImage(mineralFilename, miningClassifier, miningFilename):

    """
    Classify a mineral-classified image using a trained mining classifier and save the results to a file.
    """

    # open the mineral-classified image

    # allocate an MxN array for the mining-classified image
    classifiedImage = numpy.ndarray(???)

    # for each pixel in the mineral-classified image
    for ???:

        # get the surrounding region as a multiband pixel
        mineralRegion = getRegionAsMultibandPixel(mineralDataset, x, y)

        # classify it
        classifiedImage[???] = classifyRegion(mineralRegion, miningClassifier)

    # save the mining-classified image to a file

def getRegionAsMultibandPixel(image, x, y):

    """
    Return a multiband pixel representing the region in an image surrounding a given pixel.
    """

    # get the surrounding region

    # represent the region as a multiband pixel

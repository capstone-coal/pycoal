#!/usr/bin/python
import ???

# define number of layers in normalized hyperpixel
numberOfLayers = 128

## train the neural net using the digital spectral library

# open the digital spectral library
# we may need to load it as an image instead
library = spectral.io.envi.open("/path/to/s06av95a_envi.hdr")

# normalize spectra
principalComponents = spectral.algorithms.algorithms.principal_components(???(library))
principalComponents.reduce(numberOfLayers, ???)
normalizedLibrary = principalComponents.transform(???(library))

# generate training data
trainingData = ???(normalizedLibrary)

# initialize and train a neural network using the training data
# it would be nice to find a way to save it to a file so we only train once
classifier = spectral.algorithms.classifiers.PerceptronClassifier(???)
classifier.train(trainingData, ???)

## classify an image using the trained classifier

# open the image
# naturally we could also loop over a set of images
image = spectral.io.aviris.open_image("/path/to/ang20150422t163638_???_v1e_img")

# get an iterator over pixels in the image
pixelIterator = spectral.algorithms.algorithms.ImageIterator(image)

# define a linear transformation to scale the pixel if necessary
# the scalars would presumably be read from metadata
transform = spectral.algorithms.transforms.LinearTransform(???)

# allocate a MxN array for the classified image
classifiedImage = numpy.ndarray(???)

# for each pixel in the image
for (pixel in pixelIterator)

    # transform it
    transformedPixel = transform(pixel)

    # normalize it
    principalComponents = spectral.algorithms.algorithms.principal_components(???(transformedPixel))
    principalComponents.reduce(numberOfLayers, ???)
    normalizedTransformedPixel = principalComponents.transform(pixel)

    # classify and store it in the classified image
    classifiedImage[???] = classifier.classify_spectrum(normalizedTransformedPixel[???])

# save the classified image to a file
# we can open it for viewing or use it as input for mining classification
spectral.io.envi.save_classification("classifiedImageFilename.hdr", classifiedImage, ???)

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

from subprocess import call
import spectral
import numpy
from os.path import abspath, dirname, basename, splitext
import pycoal

class EnvironmentalCorrelation:

    def __init__(self):
        """
        Construct a new ``EnvironmentalCorrelation`` object.
        """
        pass

    def intersectProximity(self, miningFilename, vectorFilename, proximity, correlatedFilename):
        """
        Generate an environmental correlation image containing pixels from the
        mining classified image detected within a given distance of features
        within a vector layer.

        Args:
            miningImage (str):     filename of the mining classified image
            vectorLayer (str):     filename of vector layer
            proximity (float):     distance in meters
            correlatedImage (str): filename of the correlated image
        """

        # get path and file names
        outputDirectory = dirname(abspath(correlatedFilename))
        miningName = splitext(basename(abspath(miningFilename)))[0]
        vectorName = splitext(basename(abspath(vectorFilename)))[0]

        # rasterize the vector features to the same dimensions as the mining image
        featureHeaderName = outputDirectory + '/' + miningName + '_' + vectorName + '.hdr'
        self.createEmptyCopy(miningFilename, featureHeaderName)
        featureImageName = featureHeaderName[:-4] + '.img'
        self.rasterize(vectorFilename, featureImageName)

        # generate a proximity map from the features
        proximityHeaderName = outputDirectory + '/' + miningName + '_' + vectorName + '_proximity.hdr'
        proximityImageName = proximityHeaderName[:-4] + '.img'
        self.proximity(featureImageName, proximityImageName)

        # load mining and proximity images and initialize environmental correlation array
        miningImage = spectral.open_image(miningFilename)
        proximityImage = spectral.open_image(proximityHeaderName)
        correlatedImage = numpy.zeros(shape=miningImage.shape, dtype=numpy.uint16)

        # get average pixel size
        if miningImage.metadata.get('map info')[10][-6:].lower() == 'meters':
            xPixelSize = float(miningImage.metadata.get('map info')[5])
            yPixelSize = float(miningImage.metadata.get('map info')[6])
            pixelSize = (xPixelSize + yPixelSize) / 2
        else:
            raise ValueError('Mining image units not in meters.')

        # intersect features within proximity
        for x in range(miningImage.shape[0]):
            for y in range(miningImage.shape[1]):
                if miningImage[x,y,0]==1 and proximityImage[x,y,0]*pixelSize<=proximity:
                    correlatedImage[x,y,0] = miningImage[x,y,0]

        # save the environmental correlation image
        spectral.io.envi.save_classification(
            correlatedFilename,
            correlatedImage,
            class_names=['No data','Data'],
            metadata={
                'data ignore value': 0,
                'description': 'PyCOAL '+pycoal.version+' environmental correlation image.',
                'map info': miningImage.metadata.get('map info')
            })

    def createEmptyCopy(self, sourceFilename, destinationFilename):
        """
        Create an empty copy of a PyCOAL classified image with the same size.

        Args:
            sourceFilename (str):      filename of the source image
            destinationFilename (str): filename of the destination image
        """

        # open the source image
        source = spectral.open_image(sourceFilename)

        # create an empty array of the same dimensions
        destination = numpy.zeros(shape=source.shape, dtype=numpy.uint16)

        # save it with source metadata
        spectral.io.envi.save_classification(
            destinationFilename,
            destination,
            class_names=['No data','Data'],
            metadata={
                'data ignore value': 0,
                'map info': source.metadata.get('map info')
            })

    def rasterize(self, vectorFilename, featureFilename):
        """
        Burn features from a vector image onto a raster image.

        Args:
            vectorFilename (str):  filename of the vector image
            featureFilename (str): filename of the raster image
        """

        # assume the layer has the same name as the image
        layerName = splitext(basename(vectorFilename))[0]

        # convert vector features into nonzero pixels of the output file
        returncode = call(['gdal_rasterize',
                           '-burn', '1',
                           '-l', layerName,
                           vectorFilename,
                           featureFilename])

        # detect errors
        if returncode != 0:
            raise RuntimeError

    def proximity(self, featureFilename, proximityFilename):
        """
        Generate a proximity map from the features.

        Args:
            featureFilename (str):   filename of the feature image
            proximityFilename (str): filename of the proximity image
        """

        # generate an ENVI proximity map with georeferenced units
        returncode = call(['gdal_proximity.py',
                           featureFilename,
                           proximityFilename,
                           '-of', 'envi'])

        # detect errors
        if returncode != 0:
            raise RuntimeError

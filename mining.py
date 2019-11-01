# Copyright (C) 2017 COAL Developers
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth 
# Floor, Boston, MA 02110-1301, USA.

import spectral
import pycoal
import numpy

# classes identified as proxies for coal mining
proxyClassNames = [u'Schwertmannite BZ93-1 s06av95a=b',
                   u'Renyolds_TnlSldgWet SM93-15w s06av95a=a',
                   u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a']

class MiningClassification:

    def __init__(self, classNames=proxyClassNames):
        """
        Construct a new MiningClassification object given an optional list of
        spectral class names which defaults to coal mining proxies.

        Args:
            classNames (str[]): list of class names to identify.
        """

        self.classNames = classNames

    def classifyImage(self, imageFilename, classifiedFilename):

        """
        Classify mines or other features in a COAL mineral classified image by
        copying relevant pixels and discarding the rest in a new file.

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
        classList = image.metadata.get('class names')
        classNums = [classList.index(className) if className in classList else -1 for className in self.classNames]

        # copy pixels of the desired classes
        for y in range(N):
            for x in range(M):
                pixel = data[x,y]
                if pixel[0] in classNums:
                    classified[x,y] = 1 + classNums.index(pixel[0])

        # save the classified image to a file
        spectral.io.envi.save_classification(
            classifiedFilename,
            classified,
            class_names=['No data']+self.classNames,
            metadata={
                'data ignore value': 0,
                'description': 'COAL '+pycoal.version+' mining classified image.',
                'map info': image.metadata.get('map info')
            })

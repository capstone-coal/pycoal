# Copyright (C) 2017-2018 COAL Developers
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

import logging
import numpy
import pycoal
import spectral
import time

# classes identified as proxies for coal mining classification using USGSv6
proxy_class_names_usgsv6 = [u'Schwertmannite BZ93-1 s06av95a=b',
                            u'Renyolds_TnlSldgWet SM93-15w s06av95a=a',
                            u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a']

# classes identified as proxies for coal mining classification using USGSv7
proxy_class_names_usgsv7 = [u'Schwertmannite BZ93-1         BECKb AREF',
                     u'Renyolds_TnlSldgWet SM93-15w  BECKa AREF',
                     u'Renyolds_Tnl_Sludge SM93-15   BECKa AREF']

class MiningClassification:

    def __init__(self, class_names=proxy_class_names_usgsv6):
        """
        Construct a new MiningClassification object given an optional list of
        spectral class names which defaults to coal mining proxies.

        Args:
            class_names (str[]): list of class names to identify.
        """

        self.class_names = class_names
        logging.info("Instantiated Mining Classifier with following specification: " \
         "-proxy class names '%s'" %(class_names))

    def classify_image(self, image_file_name, classified_file_name, spectral_version):

        """
        Classify mines or other features in a COAL mineral classified image by
        copying relevant pixels and discarding the rest in a new file.

        Args:
            image_file_name (str):      filename of the image to be classified
            classified_file_name (str): filename of the classified image

        Returns:
            None
        """
        if (spectral_version == "7"):
            class_names = proxy_class_names_usgsv7
            self.class_names = class_names
            logging.info("Instantiated Mining Classifier with following specification: " \
                     "-proxy class names '%s'" %(class_names))
        start = time.time()
        logging.info("Starting Mining Classification for image '%s', saving classified image to '%s'" 
            %(image_file_name, classified_file_name))
        # open the image
        image = spectral.open_image(image_file_name)
        data = image.asarray()
        M = image.shape[0]
        N = image.shape[1]

        # allocate a zero-initialized MxN array for the classified image
        classified = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # get class numbers from names
        class_list = image.metadata.get('class names')
        class_nums = [class_list.index(className) if className in class_list else -1 for className in self.class_names]

        # copy pixels of the desired classes
        for y in range(N):
            for x in range(M):
                pixel = data[x,y]
                if pixel[0] in class_nums:
                    classified[x,y] = 1 + class_nums.index(pixel[0])

        # save the classified image to a file
        spectral.io.envi.save_classification(
            classified_file_name,
            classified,
            class_names=['No data']+self.class_names,
            metadata={
                'data ignore value': 0,
                'description': 'COAL '+pycoal.version+' mining classified image.',
                'map info': image.metadata.get('map info')
            })

        end = time.time()
        seconds_elapsed = end - start
        m, s = divmod(seconds_elapsed, 60)
        h, m = divmod(m, 60)
        logging.info("Completed Mining Classification. Time elapsed: '%d:%02d:%02d'" % (h, m, s))

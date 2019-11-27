# Copyright (C) 2017-2019 COAL Developers
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

# See https://github.com/capstone-coal/pycoal/pull/183#issuecomment-556821753
# for more information about potential proxy classes. Also note that these
# classes are not always guaranteed indicators of mining activity.

# classes identified as proxies for coal mining classification using USGSv6
PROXY_CLASS_NAMES_USGSV6 = [u'Schwertmannite BZ93-1 s06av95a=b',
                            u'Renyolds_TnlSldgWet SM93-15w s06av95a=a',
                            u'Renyolds_Tnl_Sludge SM93-15 s06av95a=a']

# classes identified as proxies for coal mining classification using USGSv7
# TODO: Are we sure these class names are stored in unicode in the
# mineral-classified file? Maybe we shouldn't use the 'u' prefix here
PROXY_CLASS_NAMES_USGSV7 = [u'Schwertmannite BZ93-1         BECKb AREF',
                            u'Renyolds_TnlSldgWet SM93-15w  BECKa AREF',
                            u'Renyolds_Tnl_Sludge SM93-15   BECKa AREF',
                            # Halite
                            u'Halite HS433.1B              ASDFRa AREF',
                            u'Halite HS433.2B              ASDFRa AREF',
                            u'Halite HS433.3B               BECKa AREF',
                            u'Halite HS433.3B              ASDFRa AREF',
                            u'Halite HS433.3B             NIC4aau RREF',
                            u'Halite HS433.4B              ASDFRa AREF',
                            u'Halite HS433.6               ASDFRa AREF',
                            # Muscovite
                            u'Muscovite CU93-1 low-Al Phyl  NIC4b RREF',
                            u'Muscovite GDS107              BECKa AREF',
                            u'Muscovite GDS107             NIC4aa RREF',
                            u'Muscovite GDS108              BECKb AREF',
                            u'Muscovite GDS108             NIC4bb RREF',
                            u'Muscovite GDS111 Guatemala    BECKa AREF',
                            u'Muscovite GDS111 Guatemala  NIC4aaa RREF',
                            u'Muscovite GDS113 Ruby         BECKa AREF',
                            u'Muscovite GDS113 Ruby        ASDNGa AREF',
                            u'Muscovite GDS113a Ruby       ASDNGa AREF',
                            u'Muscovite GDS113 Ruby       NIC4aaa RREF',
                            u'Muscovite GDS114 Marshall     BECKa AREF',
                            u'Muscovite GDS114 Marshall   NIC4aaa RREF',
                            u'Muscovite GDS116 Tanzania     BECKa AREF',
                            u'Muscovite GDS116a Tanzania   ASDNGa AREF',
                            u'Muscovite GDS116 Tanzania    ASDNGa AREF',
                            u'Muscovite GDS116 Tanzania   NIC4aaa RREF',
                            u'Muscovite GDS117 Isinglas     BECKa AREF',
                            u'Muscovite GDS117 Isingles   NIC4aaa RREF',
                            u'Muscovite GDS118 Capitan      BECKa AREF',
                            u'Muscovite GDS118 Capitan    NIC4aaa RREF',
                            u'Muscovite GDS119 Mt Alamo     BECKa AREF',
                            u'Muscovite GDS119 Mt Alamo    NIC4aa RREF',
                            u'Muscovite GDS120 Pegma M.     BECKa AREF',
                            u'Muscovite GDS120 Pegma M.    NIC4aa RREF',
                            u'Muscovite HS146.1B           ASDFRa AREF',
                            u'Muscovite HS146.3B            BECKa AREF',
                            u'Muscovite HS146.3B           ASDFRa AREF',
                            u'Muscovite HS146.3B          NIC4aaa RREF',
                            u'Muscovite HS146.4B           ASDFRa AREF',
                            u'Muscovite HS24.3              BECKb AREF',
                            u'Muscovite HS24.3            NIC4bbu RREF',
                            u'Muscovite IL107               BECKb AREF',
                            u'Muscov+Jaros CU93-314 coatng  BECKb AREF',
                            u'Muscov+Jaros CU93-314 coatng ASDNGb AREF',
                            # Kieserite
                            u'Kieserite KIEDE1.a crse gr   ASDFRc AREF',
                            u'Kieserite KIEDE1.a crse gr   NIC4cc AREF',
                            u'Kieserite KIEDE1.b fine gr   ASDFRc AREF',
                            # Calcite
                            u'Calcite CO2004                BECKb AREF',
                            u'Calcite GDS304 75-150um      ASDFRb AREF',
                            u'Calcite HS48.3B               BECKa AREF',
                            u'Calcite WS272                 BECKa AREF',
                            u'Calcite WS272                ASDNGa AREF',
                            u'Calcite WS272               NIC4aaa RREF',
                            u'Calcite_REE-bearing WS319a   ASDFRb AREF',
                            # Dolomite
                            u'Dolomite COD2005              BECKb AREF',
                            u'Dolomite HS102.1B            ASDNGb AREF',
                            u'Dolomite HS102.3B             BECKb AREF',
                            u'Dolomite HS102.3B            ASDNGb AREF',
                            u'Dolomite HS102.3B           NIC4bbb RREF',
                            u'Dolomite HS102.4B            ASDNGb AREF',
                            u'Dolomite ML97-3 Ferroan      ASDFRb AREF',
                            # Wollastonite
                            u'Wollastonite HS348.1B        ASDFRc AREF',
                            u'Wollastonite HS348.2B        ASDFRc AREF',
                            u'Wollastonite HS348.3B         BECKc AREF',
                            u'Wollastonite HS348.3B        ASDFRc AREF',
                            u'Wollastonite HS348.3B       NIC4ccc RREF',
                            u'Wollastonite HS348.4B        ASDFRb AREF',
                            # Lead
                            u'Lead-tin_yellow GDS793       ASDFRa AREF',
                            u'Lead_White GDS796            ASDFRa AREF',
                            # Cadmium
                            u'Cadmium_orange_0      GDS786 ASDFRa AREF',
                            u'Cadmium_orange_1 (dk) GDS781 ASDFRa AREF',
                            u'Cadmium_red_2 GDS778         ASDFRa AREF',
                            u'Cadmium_yellow_6 med GDS788  ASDFRa AREF',
                            # Pyrite
                            u'Arsenopyrite HS262.1B        ASDFRc AREF',
                            u'Arsenopyrite HS262.2B        ASDFRc AREF',
                            u'Arsenopyrite HS262.3B         BECKc AREF',
                            u'Arsenopyrite HS262.3B        ASDFRc AREF',
                            u'Arsenopyrite HS262.3B       NIC4cdu RREF',
                            u'Arsenopyrite HS262.4B        ASDFRc AREF',
                            u'Chalcopyrite HS431.1B        ASDFRb AREF',
                            u'Chalcopyrite HS431.2B        ASDFRb AREF',
                            u'Chalcopyrite HS431.3B         BECKb AREF',
                            u'Chalcopyrite HS431.3B        ASDFRb AREF',
                            u'Chalcopyrite HS431.3B        NIC4bc RREF',
                            u'Chalcopyrite HS431.4B        ASDFRb AREF',
                            u'Chalcopyrite S26-36           BECKb AREF',
                            u'Pyrite GDS483.c 30-60um      ASDFRc AREF',
                            u'Pyrite GDS483.c 30-60um     NIC4cdb RREF',
                            u'Pyrite HS35.3                 BECKb AREF',
                            u'Pyrite HS35.3                NIC4cc RREF',
                            u'Pyrite S142-1                 BECKc AREF',
                            u'Pyrite S26-8                  BECKc AREF',
                            u'Pyrite S29-4                  BECKc AREF',
                            u'Pyrite S30                    BECKc AREF',
                            # Gypsum
                            u'Gypsum HS333.1B (Selenite)   ASDFRa AREF',
                            u'Gypsum HS333.2B (Selenite)   ASDFRa AREF',
                            u'Gypsum HS333.3B (Selenite)    BECKa AREF',
                            u'Gypsum HS333.3B (Selenite)   ASDFRa AREF',
                            u'Gypsum HS333.3B (Selenite)   ASDNGa AREF',
                            u'Gypsum HS333.3B (Selenite)  NIC4aaa RREF',
                            u'Gypsum HS333.4B (Selenite)   ASDFRa AREF',
                            u'Gypsum SU2202                 BECKa AREF',
                            # Taken directly from mine tailings or waste 
                            # rock - highly indicative of mining!
                            u'Pyrite LV95-6A Weath on Tail  BECKb AREF',
                            u'Blck_Mn_Coat_Tailngs LV95-3   BECKb AREF']


class MiningClassification:

    def __init__(self, class_names=None):
        """
        Construct a new MiningClassification object given an optional list of
        spectral class names which defaults to coal mining proxies.

        Args:
            class_names (str[]): list of class names to identify.
        """

        if class_names is None:
            class_names = PROXY_CLASS_NAMES_USGSV7
        self.class_names = class_names
        logging.info(
            "Instantiated Mining Classifier with following specification: "
            "-proxy class names '%s'", class_names)

    def classify_image(self, image_file_name, classified_file_name,
                       spectral_version):

        """
        Classify mines or other features in a COAL mineral classified image by
        copying relevant pixels and discarding the rest in a new file.

        Args:
            image_file_name (str):      filename of the image to be classified
            classified_file_name (str): filename of the classified image
            spectral_version (str:      version of Spectral library to use

        Returns:
            None
        """
        class_names = PROXY_CLASS_NAMES_USGSV6 if spectral_version == "6" \
            else PROXY_CLASS_NAMES_USGSV7
        self.class_names = class_names
        logging.info(
            "Instantiated Mining Classifier with following "
            "specification: "
            "-proxy class names '%s'", class_names)
        start = time.time()
        logging.info(
            "Starting Mining Classification for image '%s', saving "
            "classified image to '%s'", image_file_name, classified_file_name)
        # open the image
        image = spectral.open_image(image_file_name)
        data = image.asarray()
        m = image.shape[0]
        n = image.shape[1]

        # allocate a zero-initialized MxN array for the classified image
        classified = numpy.zeros(shape=(m, n), dtype=numpy.uint16)

        # get class numbers from names
        class_list = image.metadata.get('class names')
        class_nums = [
            class_list.index(className) if className in class_list else -1 for
            className in self.class_names]

        # copy pixels of the desired classes
        for y in range(n):
            for x in range(m):
                pixel = data[x, y]
                if pixel[0] in class_nums:
                    classified[x, y] = 1 + class_nums.index(pixel[0])

        # save the classified image to a file
        spectral.io.envi.save_classification(classified_file_name, classified,
                                             class_names=['No data'] +
                                             self.class_names,
                                             metadata={'data ignore value': 0,
                                                       'description': 'COAL '
                                                       '' + pycoal.version +
                                                       ' mining ' +
                                                       'classified image.',
                                                       'map info':
                                                           image.metadata.get(
                                                            'map info')})

        end = time.time()
        seconds_elapsed = end - start
        m, s = divmod(seconds_elapsed, 60)
        h, m = divmod(m, 60)
        logging.info(
            "Completed Mining Classification. Time elapsed: '%d:%02d:%02d'",
            h, m, s)

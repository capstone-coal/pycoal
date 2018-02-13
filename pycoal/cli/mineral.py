# Copyright (C) 2018 COAL-FO Developers
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
# encoding: utf-8
''' 
https://capstone-coal.github.io/docs#usage
@author:     COAL Developers
@copyright:  2018 COAL Developers. All rights reserved.
@license:    GNU General Public License version 2
@contact:    coal-capstone@googlegroups.com
'''
import sys
import os
import re
from sys import path
from os import getcwd
import inspect
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import sys
import os
import pycoal
sys.path.insert(0, '../')
import mineral
import logging
import math
import numpy
import spectral
import time

__all__ = []

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''
    logging.basicConfig(filename='pycoal.log',level=logging.INFO, format='%(asctime)s %(message)s')
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
  VERSION %s
  Copyright 2018 COAL Developers. All rights reserved.
  This program is free software; you can redistribute it and/or 
  modify it under the terms of the GNU General Public License 
  as published by the Free Software Foundation; version 2.
  This program is distributed in the hope that it will be useful, 
  but WITHOUT ANY WARRANTY; without even the implied warranty 
  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
  See the GNU General Public License for more details.
  You should have received a copy of the GNU General Public 
  License along with this program; if not, write to the Free 
  Software Foundation, Inc., 51 Franklin Street, Fifth 
  Floor, Boston, MA 02110-1301, USA.
USAGE
''' % (program_shortdesc, pycoal.version)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--image", dest="image", help="Input file to be processed")
        parser.add_argument("-s", "--slib", dest="slib", help="Spectral Library filename")
        parser.add_argument("-r", "--rgb_filename", dest="rgb_filename", help="RGB File Name")
        parser.add_argument("-c", "--classified_filename", dest="classified_filename", help="Classified File Name")

        # Process arguments
        args = parser.parse_args(['-i', '-s', 'r', 'c'])
        args = parser.parse_args()

        image = args.image
        slib = args.slib
        rgb_filename = args.rgb_filename
        classified_filename = args.classified_filename
        
        #image = "ang20150420t182050_corr_v1e_img.hdr"
        #slib = "s06av95a_envi.hdr"
        #rgb_filename = "ang20150420t182050_corr_v1e_img_rgb.hdr"
        #classified_filename = "ang20150420t182050_corr_v1e_img_class.hdr"
        
        # create a new mineral classification instance
        mineral_classification = mineral.MineralClassification(slib)

        # generate a georeferenced visible-light image
        mineral_classification.to_rgb(image, rgb_filename)

        # generate a mineral classified image
        mineral_classification.classify_image(image, classified_filename)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

        Writer(image = image, slib = slib).write()

if __name__ == '__main__':
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'mineral_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

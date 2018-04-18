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
# encoding: utf-8

'''
example_mineral -- an example script which demonstrates COAL mineral classification

example_mineral provides a CLI which demonstrates how the COAL Mineral Classification 
API provides methods for generating visible-light and mineral classified images. 
Mineral classification can take hours to days depending on the size of the spectral 
library and the available computing resources, so running a script in the background 
is recommended. More reading an this example can be seen at 
https://capstone-coal.github.io/docs#usage

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2018 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import sys
import os
from sys import path
from os import getcwd
import inspect

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import logging

import sys
import os
import pycoal
sys.path.insert(0, '../pycoal')
import mineral
import mining
import environment

__all__ = []

DEBUG = 1
TESTRUN = 0
PROFILE = 0


input_filename = 'avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2/ang20150420t182050_rfl_v1e/ang20150420t182050_corr_v1e_img.hdr'
library_filename='../pycoal/tests/s06av95a_envi.hdr'

def run_mineral(input_filename, library_filename):
    '''
    ...
    '''
    logging.info("Starting mineral classification with input file '%s' and spectral library '%s'." %(input_filename, library_filename))
    # path to save RGB image
    rgb_filename = "ang20150420t182050_corr_v1e_img_rgb.hdr"

    # path to save mineral classified image
    classified_filename = "ang20150420t182050_corr_v1e_img_class.hdr"

    # create a new mineral classification instance
    mineral_classification = mineral.MineralClassification(library_filename)

    # generate a georeferenced visible-light image
    mineral_classification.to_rgb(input_filename, rgb_filename)

    # generate a mineral classified image
    mineral_classification.classify_image(input_filename, classified_filename)

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

  Copyright (C) 2017-2018 COAL Developers

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
        parser.add_argument("-i", "--image", dest="image", default=input_filename, help="Input file to be processed [default: ang20150420t182050_corr_v1e_img.hdr]")
        parser.add_argument("-s", "--slib", dest="slib", default=library_filename, help="Spectral Library filename [default: s06av95a_envi.hdr]")

        # Process arguments
        args = parser.parse_args(['-i', input_filename, '-s', library_filename])
        #args = parser.parse_args()

        image = args.image
        slib = args.slib
        
        run_mineral(image, slib)

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

if __name__ == "__main__":
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
        profile_filename = 'example_mineral_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

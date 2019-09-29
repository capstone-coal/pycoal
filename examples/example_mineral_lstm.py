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
# encoding: utf-8

'''
example_mineral_lstm -- an example script which demonstrates COAL mineral classification
                        using a binary classifier based on Recurrent Neural Network

example_mineral_lstm provides a CLI which demonstrates how the COAL Mineral Classification 
API provides methods for generating visible-light and mineral classified images. 
Mineral classification can take hours to days depending on the size of the spectral 
library and the available computing resources, so running a script in the background 
is recommended. More reading an this example can be seen at 
https://capstone-coal.github.io/docs#usage

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2019 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import logging

import sys
import os
import constants
import pycoal
from pycoal import mineral

model_filename = "../pycoal/tests/nn_models/lstm_Schwertmannite.h5"

def run_mineral(input_filename, library_filename):
    logging.info("Starting mineral classification with input file '%s' and spectral library '%s'." %(input_filename, library_filename))
    # path to save RGB image
    rgb_filename = constants.INPUT_NAME + "_rgb.hdr"
    
    # path to save mineral classified image
    classified_filename = constants.INPUT_NAME + "_class.hdr"

    # path to save classification scores image
    scores_filename = constants.INPUT_NAME + "_scores.hdr"

    # list containing the names of all considered classification classes
    class_names = ["Schwertmannite","non-Schwertmannite"]
    
    # create a new mineral classification instance
    mineral_classification = mineral.MineralClassification(algorithm=mineral.avngDNN, model_file_name=model_filename, class_names=class_names, scores_file_name=scores_filename)

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

    program_name = os.path.basename(argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  VERSION %s

  Copyright (C) 2017-2019 COAL Developers

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
        parser.add_argument("-i", "--image", dest="image", default=constants.INPUT_FILENAME,
                            help="Input file to be processed [default: " + constants.INPUT_FILENAME + "]")
        parser.add_argument("-s", "--slib", dest="slib", default=constants.LIBRARY_FILENAME,
                            help="Spectral Library filename [default: " + constants.LIBRARY_FILENAME + "]")

        # Process arguments
        args = parser.parse_args(['-i', constants.INPUT_FILENAME, '-s', constants.LIBRARY_FILENAME])

        image = args.image
        slib = args.slib

        run_mineral(image, slib)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if constants.DEBUG or constants.TESTRUN:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if constants.DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if constants.TESTRUN:
        import doctest
        doctest.testmod()
    if constants.PROFILE:
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

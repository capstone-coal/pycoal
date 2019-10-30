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
example_mining -- an example script which demonstrates COAL mining
classification

example_mining provides a CLI which demonstrates how the COAL Mining
Classification
API filters mineral classified images to identify specific classes of
interest,
by default proxies for coal mining in the USGS Digital Spectral Library 06. 
More reading an this example can be seen at 
https://capstone-coal.github.io/docs#usage

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2019 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import logging

import constants
import pycoal
from pycoal import mining

'''
    # path to mineral classified image
    mineral_filename = constants"ang20150420t182050_corr_v1e_img_class.hdr"

    # path to save mining classified image
    mining_filename = "ang20150420t182050_corr_v1e_img_class_mining.hdr"
    
    #Spectral Library Verison Number, Change to 7 if you want to use USGS 
    Spectral Library Version 7
'''


def run_mining(mineral_filename=constants.INPUT_NAME + "_class.hdr",
               mining_filename=constants.INPUT_NAME + "_mining.hdr",
               spectral_version="6"):
    """Run mining classification.

    :param mineral_filename: The name of the mineral file
    :param mining_filename: The name of the mining file
    :param spectral_version: 6 by default. Use 7 if you want to use USGS
    Spectral Library Version 7
    """

    # create a new mining classification instance
    mining_classification = mining.MiningClassification()

    # generate a mining classified image
    mining_classification.classify_image(mineral_filename, mining_filename,
                                         spectral_version)


def main(argv=None):  # IGNORE:C0111
    # Command line options
    logging.basicConfig(filename='pycoal.log', level=logging.INFO,
                        format='%(asctime)s %(message)s')
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
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
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-mi", "--mineral_input", dest="input",
                            default=constants.INPUT_NAME + "_class.hdr",
                            help="Input classified mineral file to be "
                                 "processed [default: " +
                                 constants.INPUT_NAME + "_class.hdr]")
        parser.add_argument("-mo", "--mining_output", dest="output",
                            default=constants.INPUT_NAME + "_class_mining.hdr",
                            help="Output mining classified image filename ["
                                 "default: " + constants.INPUT_NAME +
                                 "_class_mining.hdr]")
        parser.add_argument("-v", "--spectral_version",
                            dest="spectral_version", default='6',
                            help="USGS Spectral Library Version Number")

        # Process arguments
        args = parser.parse_args(
            ['-mi', constants.INPUT_NAME + "_class.hdr", '-mo',
             constants.INPUT_NAME + "_class_mining.hdr", '-v', '6'])
        # args = parser.parse_args()

        mineral_filename = args.input
        mining_filename = args.output
        spectral_version = args.spectral_version

        run_mining(mineral_filename, mining_filename, spectral_version)
        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
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

        profile_filename = 'example_mining_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

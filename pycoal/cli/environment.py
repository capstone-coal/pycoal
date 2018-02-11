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
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
from subprocess import call
import spectral
import numpy
from os.path import abspath, dirname, basename, splitext
import pycoal
import time
sys.path.insert(0, '../pycoal')
import mineral
import mining
import environment

__all__ = []

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''
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
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-m", "--mining",
            dest="mining_filename",
            help="Input mining classified file to be processed")
        parser.add_argument(
            "-hy", "--hydrography",
            dest="vector_filename",
            help="Path to hydrography data")
        parser.add_argument(
            "-e", "--environment",
            dest="correlation_filename",
            help="Output environmental correlation image")

        # Process arguments
        args = parser.parse_args(['-m','-hy','-e'])

        mining_filename = args.mining_filename
        vector_filename = args.vector_filename
        correlation_filename = args.correlation_filename
        # create a new environmental correlation instance
        environmental_correlation = environment.EnvironmentalCorrelation()
        # generate an environmental correlation image of mining
        # pixels within 10 meters of a stream
        environmental_correlation.intersect_proximity(mining_filename, vector_filename, 10.0, correlation_filename)

    except KeyboardInterrupt:
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

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
        profile_filename = 'environment_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
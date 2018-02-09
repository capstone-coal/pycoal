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
# encoding: utf-8
'''
example_environment -- an example script which demonstrates COAL 
environmental classification
example_environment provides a CLI which demonstrates how the 
COAL Environmental Classification API finds pixels in a mining
classified image that are within a certain number of meters
from features in a vector layer such as flow lines in the
National Hydrography Dataset (NHD).
More reading an this example can be seen at 
https://capstone-coal.github.io/docs#usage
@author:     COAL Developers
@copyright:  2017 COAL Developers. All rights reserved.
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

from pycoal.write import Writer
from pycoal.read_netcdf import NetCDFReader as Reader

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
  Copyright 2017 COAL Developers. All rights reserved.
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
            default='ang20150420t182050_corr_v1e_img_class_mining.hdr',
            help="Input mining classified file to be processed [default: ang20150420t182050_corr_v1e_img_class_mining.hdr]")
        parser.add_argument(
            "-hy", "--hydrography",
            dest="vector_filename",
            default='Shape/NHDFlowline.shp',
            help="Path to hydrography data [default: Shape/NHDFlowline.shp]")
        parser.add_argument(
            "-e", "--environment",
            dest="correlation_filename",
            default='ang20150420t182050_corr_v1e_img_class_mining_NHDFlowline_correlation.hdr',
            help="Output environmental correlation image [default: ang20150420t182050_corr_v1e_img_class_mining_NHDFlowline_correlation.hdr]")

        # Process arguments
        args = parser.parse_args(
            ['-m', 'ang20150420t182050_corr_v1e_img_class_mining.hdr',
            '-hy', 'Shape/NHDFlowline.shp',
            '-e', 'ang20150420t182050_corr_v1e_img_class_mining_NHDFlowline_correlation.hdr'])

        mining_filename = args.mining_filename
        vector_filename = args.vector_filename
        correlation_filename = args.correlation_filename

        run_environment(mining_filename, vector_filename, correlation_filename)

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
    main()
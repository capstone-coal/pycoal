#!/usr/bin/python
# -*- coding: utf-8 -*-
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
program_license = \
    '''%s
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
        '''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import logging

import pycoal
sys.path.insert(0, '../')
import mineral
import mining
import environment


def main(argv=None):

      # Setup argument parser

    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-m', '--mining', dest='mining_filename',
                        help='Input mining classified file to be processed'
                        )
    parser.add_argument('-hy', '--hydrography', dest='vector_filename',
                        help='Path to hydrography data')
    parser.add_argument('-e', '--environment',
                        dest='correlation_filename',
                        help='Output environmental correlation image')

      # Process arguments

    args = parser.parse_args()
    mining_filename = args.mining_filename
    vector_filename = args.vector_filename
    correlation_filename = args.correlation_filename

       # create a new environmental correlation instance

    environmental_correlation = environment.EnvironmentalCorrelation()

    # generate an environmental correlation image of mining
    # pixels within 10 meters of a stream

    environmental_correlation.intersect_proximity(mining_filename,
            vector_filename, 10.0, correlation_filename)


if __name__ == '__main__':
    main()

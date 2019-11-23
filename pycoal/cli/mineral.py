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

program_description = '''
pycoal-mineral -- a CLI for COAL mineral classification

pycoal-mineral provides a CLI which demonstrates how the COAL Mineral
Classification API provides methods for generating visible-light and mineral
classified images. Mineral classification can take hours to days depending on
the size of the spectral library and the available computing resources, so
running a script in the background is recommended. More reading an this
example can be seen at https://capstone-coal.github.io/docs#usage

@author:     COAL Developers

@copyright:  Copyright (C) 2017-2019 COAL Developers

@license:    GNU General Public License version 2

@contact:    coal-capstone@googlegroups.com
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pycoal.mineral import MineralClassification


def main():
    # Setup argument parser
    parser = ArgumentParser(description=program_description,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--image", dest="image",
                        help="Input file to be processed")
    parser.add_argument("-s", "--slib", dest="slib",
                        help="Spectral Library filename")
    parser.add_argument("-r", "--rgb_filename", dest="rgb_filename",
                        help="RGB File Name")
    parser.add_argument("-c", "--classified_filename",
                        dest="classified_filename",
                        help="Classified File Name")
    parser.add_argument("-cf", "--config_filename", dest="config_filename",
                        help="Configuration File Name")

    # Process arguments
    args = parser.parse_args()

    image = args.image
    slib = args.slib
    rgb_filename = args.rgb_filename
    classified_filename = args.classified_filename
    config_filename = args.config_filename

    # create a new mineral classification instance
    mineral_classification = MineralClassification(slib, config_filename)

    # generate a georeferenced visible-light image
    mineral_classification.to_rgb(image, rgb_filename)

    # generate a mineral classified image
    mineral_classification.classify_image(image, classified_filename)


if __name__ == '__main__':
    main()

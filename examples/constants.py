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

DEBUG = 0
TESTRUN = 0
PROFILE = 0

# TODO: Also demonstrate this functionality in a Jupyter Notebook

# File used if TESTRUN is set to 1.
# Contains hyperspectral data that is 0.15GB when unpacked.
# It will run relatively quickly but may have less meaningful data
# to analyze (fewer coal mines, etc.) than the large input file.
# Direct download link:
# ftp://avoil:Gulf0il$pill@popo.jpl.nasa.gov/y18_data/f180201t01p00r05.tar.gz
# Note that wget may not work with this FTP link due to the login credentials.
# Use your browser to download it by navigating to the link. Then move the
# file into the examples directory
# and unzip it (tar -xzf f180201t01p00r05.tar.gz)
SMALL_INPUT_NAME = "f180201t01p00r05rdn_e_sc01_ort_img"
SMALL_INPUT_FILE = "f180201t01p00r05rdn_e/" + SMALL_INPUT_NAME + ".hdr"

# File to use if TESTRUN is set to 0.
# Contains hyperspectral data that is ~18GB when unpacked
# Direct download link: ftp://avng.jpl.nasa.gov/AVNG_2015_data_distribution
# /L2/ang20150420t182050_rfl_v1e/
LARGE_INPUT_NAME = "ang20150420t182050_corr_v1e_img"
LARGE_INPUT_FILE = "avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2" \
                   "/ang20150420t182050_rfl_v1e/" + LARGE_INPUT_NAME + ".hdr"

# Use the smaller file is TESTRUN = 1, and the larger file if TESTRUN = 0
INPUT_NAME = SMALL_INPUT_NAME if TESTRUN else LARGE_INPUT_NAME
INPUT_FILENAME = SMALL_INPUT_FILE if TESTRUN else LARGE_INPUT_FILE

# Spectral library file name - change LIBRARY_FILENAME to 6 or 7 depending
# on which version you want to use
LIBRARY_FILENAME_6 = "s06av95a_envi.hdr"
LIBRARY_FILENAME_7 = "s07_AV95_envi.hdr"
LIBRARY_FILENAME = "../pycoal/tests/" + LIBRARY_FILENAME_7

# If you want to only classify a subset of the image, specify the range of
# rows and columns to classify.
# Set to None to classify the entire image.
# Only applies to example_mineral.py
# For reference, the small image has the shape 931X339 (931 rows and 339
# columns). This would translate to [0, 931] rows and [0, 339] columns below
MINERAL_SUBSET_ROWS = None
MINERAL_SUBSET_COLS = None

# Paths to the flowlines of streams and whatever other hydrography data
# should be correlated with a mining classified image.
# Note that the path should be relative to where you're running the
# examples from. These defaults assume that you're running
# `python3 example_environment.py` from the root project directory.
ENVIRONMENT_VECTOR_PATHS = ["pycoal/tests/images/NHDFlowline_cut.shp",
                            "pycoal/tests/images/GRanD_dams_v1_1.shp",
                            "pycoal/tests/images/GRanD_reservoirs_v1_1.shp"]

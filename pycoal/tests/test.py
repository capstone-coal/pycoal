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

import os
import ftplib

# utility function to remove multiple test files
def _remove_files(listOfFileNames):
    for fileName in listOfFileNames:
        try:
            os.remove(fileName)
        except OSError:
            pass

# file names of USGS Digital Spectral Library 06 in ENVI format
libraryFilenames = ["s06av95a_envi.hdr", "s06av95a_envi.sli"]

# set up test module before running tests
def setup_module(module):

    # enter test directory
    os.chdir('pycoal/tests')

    # download spectral library over FTP if necessary
    if not os.path.isfile(libraryFilenames[0]) and \
       not os.path.isfile(libraryFilenames[1]):
        ftp_url = "ftpext.cr.usgs.gov"
        ftp_dir = "pub/cr/co/denver/speclab/pub/spectral.library/splib06.library/Convolved.libraries/"
        ftp = ftplib.FTP(ftp_url)
        ftp.login()
        ftp.cwd(ftp_dir)
        for f in libraryFilenames:
            with open("" + f, "wb") as lib_f:
                ftp.retrbinary('RETR %s' % f, lib_f.write)

# tear down test module after running tests
def teardown_module(module):

    # leave test directory
    os.chdir('../..')

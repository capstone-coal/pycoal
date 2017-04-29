# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

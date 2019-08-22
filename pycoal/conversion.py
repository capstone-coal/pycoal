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

import os
import numpy
import spectral
import fnmatch
import shutil

class AsterToENVIConversion:

    def __init__(self):
        """
        This class provides a method for converting the `ASTER Spectral
        Library Version 2.0 <https://asterweb.jpl.nasa.gov/>`_ into ENVI format.

        Args:
            None
        """
        pass

    @classmethod
    def convert(cls, data_dir="", db_file="", hdr_file=""):
        """
        This class method generates an ENVI format spectral library file.
        ``data_dir`` is optional as long as ``db_file`` is provided. Note that
        generating an SQLite database takes upwards of 10 minutes and creating
        an ENVI format file takes up to 5 minutes. Note: This feature is still
        experimental.

        Args:
            data_dir (str, optional): path to directory containing ASCII data files
            db_file (str):            name of the SQLite file that either already exists if
                                      ``data_dir`` isn't provided, or will be generated if
                                      ``data_dir`` is provided
            hdr_file (str):           name of the ENVI spectral library to generate
                                      (without the ``.hdr`` or ``.sli`` extension)
        """
        if not hdr_file:
            raise ValueError("Must provide path for generated ENVI header file.")

        elif not db_file:
            raise ValueError("Must provide path for sqlite file.")

        if data_dir:
            spectral.AsterDatabase.create(db_file, data_dir)

        aster_database = spectral.AsterDatabase(db_file)
        spectrum_ids = [x[0] for x in aster_database.query('SELECT SampleID FROM Samples').fetchall()]
        band_min = 0.38315
        band_max = 2.5082
        band_num = 128
        band_info = spectral.BandInfo()
        band_info.centers = numpy.arange(band_min, band_max, (band_max - band_min) / band_num)
        band_info.band_unit = 'micrometer'
        library = aster_database.create_envi_spectral_library(spectrum_ids, band_info)

        library.save(hdr_file)

class USGSSpectral7ToAsterConversion:
    
    def __init__(self):
        """
            This class provides a method for converting `USGS Spectral Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ .txt files into ASTER Spectral
            Library Version 2.0 <https://asterweb.jpl.nasa.gov/> .txt files
            
            Args:
                none
            """
        pass
    
    @classmethod
    def convert(cls, library_filename=""):
        """
            This class method converts a `USGS Spectral Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ .txt file into
            an `ASTER Spectral Library Version 2.0 <https://asterweb.jpl.nasa.gov/>`_ .spectrum.txt file
            ASTER Library Version 2.0 Spectral Library files are in .spectrum.txt file format
            
            Spectral Library Version 7 can be downloaded `here <https://speclab.cr.usgs.gov/spectral-lib.html>`_
            
            Args:
                library_filename (str): path to Spectral File you wish to convert
            """
        if not library_filename:
            raise ValueError("Must provide path for Spectral File.")
        
        line_count = 1
        with open(library_filename,'r') as input_file:
            for line_count, l in enumerate(input_file):
                pass
            
        input_file = open(library_filename,'r')
        #Read Name of Spectra on first line of the file
        spectra_line = input_file.readline()
        spectra_name = spectra_line[23:]
        k = 0
        #Loop through file and store all wavelength values for the given Spectra
        spectra_values_file = open('SpectraValues.txt','w')
        spectra_wave_length = 0
        while(k < line_count):
            spectra_wave_length = float(input_file.readline()) * 100
            spectra_wave_length = spectra_wave_length / 1000
            spectra_wave_length = float("{0:.5f}".format(spectra_wave_length))
            spectra_y_value = spectra_wave_length * 10
            line = str(spectra_wave_length) + '  ' + str(spectra_y_value)
            spectra_values_file.write(line)
            spectra_values_file.write('\n')
            k = k+1
        #Write new file in the form of an ASTER .spectrum.txt file while using stored
        #Spectra Name and stored Spectra Wavelength values`
        input_file = open(library_filename,'w')
        input_file.write('Name:')
        input_file.write(spectra_name)
        input_file.write('Type:\n')
        input_file.write('Class:\n')
        input_file.write('Subclass:\n')
        input_file.write('Particle Size:  Unknown\n')
        input_file.write('Sample No.:  0000000000\n')
        input_file.write('Owner:\n')
        input_file.write('Wavelength Range:  ALL\n')
        input_file.write('Origin: Spectra obtained from the Noncoventional Exploitation Factors\n')
        input_file.write('Data System of the National Photographic Interpretation Center.\n')
        input_file.write('Description:  Gray and black construction asphalt.  The sample was\n')
        input_file.write('soiled and weathered, with some limestone and quartz aggregate\n')
        input_file.write('showing.\n')
        input_file.write('\n')
        input_file.write('\n')
        input_file.write('\n')
        input_file.write('Measurement:  Unknown\n')
        input_file.write('First Column:  X\n')
        input_file.write('Second Column: Y\n')
        input_file.write('X Units:  Wavelength (micrometers)\n')
        input_file.write('Y Units:  Reflectance (percent)\n')
        input_file.write('First X Value:\n')
        input_file.write('Last X Value:\n')
        input_file.write('Number of X Values:\n')
        input_file.write('Additional Information:\n')
        input_file.write('\n')
        j = 0
        spectra_values_file.close()
        #Read in values saved in SpectraValues.txt and output them to the library_filename
        spectra_values_file = open('SpectraValues.txt','r')
        while(j < line_count):
            spectra_wave_length = spectra_values_file.readline()
            input_file.write(spectra_wave_length)
            j = j+1
        #Close all open files
        input_file.close()
        spectra_values_file.close()
        #Rename library_filename to match ASTER .spectrum.txt file format
        os.rename(library_filename,library_filename + '.spectrum.txt')
        #Remove temporary file for storing wavelength data
        os.remove('SpectraValues.txt')

class FullUSGSSpectral7ToENVIConversion:
    def __init__(self):
        """
            This class method converts the entire `USGS Spectral Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ library into
            its convolved envi format
            
            Args:
                none
            """
        pass

    @classmethod
    def convert(cls, library_filename=""):
        """
            This class method converts the entire `USGS Spectral Library Version 7
            <https://speclab.cr.usgs.gov/spectral-lib.html>`_ library into
            its convolved envi format
            
            Spectral Library Version 7 can be downloaded `here <https://speclab.cr.usgs.gov/spectral-lib.html>`_
            
            Args:
            library_filename (str): path to USGS Spectral Library Version 7 directory
            """
        if not library_filename:
            raise ValueError("Must provide path for USGS Spectral Library Version 7.")
        
        #This will take all the necessary .txt files for spectra in USGS
        #Spectral Library Version 7 and put them in a new directory called
        #"usgs_splib07_modified" in the examples directory
        directory = 'usgs_splib07_modified'
        if not os.path.exists(directory):
            os.makedirs(directory)

        for root, dir, files in os.walk(library_filename + "/ASCIIdata"):
            dir[:] = [d for d in dir]
            for items in fnmatch.filter(files, "*.txt"):
                if "Bandpass" not in items:
                    if "errorbars" not in items:
                        if "Wave" not in items:
                            if "SpectraValues" not in items:
                                shutil.copy2(os.path.join(root,items), directory)

        #This will take the .txt files for Spectra in USGS Spectral Version 7 and
        #convert their format to match that of ASTER .spectrum.txt files for spectra
        # create a new mineral aster conversion instance
        spectral_aster = USGSSpectral7ToAsterConversion()
        #List to check for duplicates
        spectra_list = []
        # Convert all files
        files = os.listdir(directory +'/')
        for x in range(0, len(files)):
            name = directory+'/' + files[x]
            #Get name
            input_file = open(name,'r')
            spectra_line = input_file.readline()
            spectra_cut = spectra_line[23:]
            spectra_name = spectra_cut[:-14]
            #Remove first and last char in case extra spaces are added
            spectra_first_space = spectra_name[1:]
            spectra_last_space = spectra_first_space[:-1]
            
            #Check if Spectra is unique
            set_spectra = set(spectra_list)
            if not any(spectra_name in s for s in set_spectra):
                if not any(spectra_last_space in a for a in set_spectra):
                    spectral_aster.convert(name)
                    spectra_list.append(spectra_name)

        set_spectra = set(spectra_list)
        print(set_spectra)

        #This will generate three files s07AV95a_envi.hdr, s07AV95a_envi.hdr.sli,splib.db and dataSplib07.db
        #For a library in `ASTER Spectral Library Version 2.0 <https://asterweb.jpl.nasa.gov/>`_ format
        data_dir = "dataSplib07.db"
        #Avoid overwrite during nosetests of full .hdr and .sli files with sample .hdr and .sli
        if (os.path.isfile('s07_AV95_envi.hdr')):
            header_name = "s07_AV95_envi_sample"
        else :
            header_name = "s07_AV95_envi"
        # create a new mineral aster conversion instance
        spectral_envi = AsterToENVIConversion()
        # Generate .sli and .hdr
        spectral_envi.convert(directory,data_dir,header_name)


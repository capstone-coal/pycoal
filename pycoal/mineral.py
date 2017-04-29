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

import math
import numpy
import spectral
import pycoal

class MineralClassification:

    def __init__(self, libraryFilename, classNames=None, threshold=0.0, inMemory=False):
        """
        Construct a new ``MineralClassification`` object with a spectral library
        in ENVI format such as the `USGS Digital Spectral Library 06
        <https://speclab.cr.usgs.gov/spectral.lib06/>`_ or the `ASTER Spectral
        Library Version 2.0 <https://speclib.jpl.nasa.gov/>`_ converted with
        ``pycoal.mineral.AsterConversion.convert()``.

        If provided, the optional class name parameter will initialize the
        classifier with a subset of the spectral library, otherwise the full
        spectral library will be used.

        The optional threshold parameter defines a confidence value between zero
        and one below which classifications will be discarded, otherwise all
        classifications will be included.

        In order to improve performance on systems with sufficient memory,
        enable the optional parameter to load entire images.

        Args:
            libraryFilename (str):        filename of the spectral library
            classNames (str[], optional): list of names of classes to include
            threshold (float, optional):  classification threshold
            inMemory (boolean, optional): enable loading entire image
        """

        # load and optionally subset the spectral library
        self.library = spectral.open_image(libraryFilename)
        if classNames is not None:
            self.library = self.subsetSpectralLibrary(self.library, classNames)

        # store the threshold
        self.threshold = threshold

        # store the memory setting
        self.inMemory = inMemory

    def classifyImage(self, imageFilename, classifiedFilename):
        """
        Classify minerals in an AVIRIS image using spectral angle mapper
        classification and save the results to a file.

        Args:
            imageFilename (str):      filename of the image to be classified
            classifiedFilename (str): filename of the classified image

        Returns:
            None
        """

        # open the image
        image = spectral.open_image(imageFilename)
        if self.inMemory:
            data = image.load()
        else:
            data = image.asarray()
        M = image.shape[0]
        N = image.shape[1]

        # define a resampler
        # TODO detect and scale units
        # TODO band resampler should do this
        resample = spectral.BandResampler([x/1000 for x in image.bands.centers],
                                          self.library.bands.centers)

        # allocate a zero-initialized MxN array for the classified image
        classified = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # for each pixel in the image
        for x in range(M):

            for y in range(N):

                # read the pixel from the file
                pixel = data[x,y]

                # if it is not a no data pixel
                if not numpy.isclose(pixel[0], -0.005) and not pixel[0]==-50:

                    # resample the pixel ignoring NaNs from target bands that don't overlap
                    # TODO fix spectral library so that bands are in order
                    resampledPixel = numpy.nan_to_num(resample(pixel))

                    # calculate spectral angles
                    angles = spectral.spectral_angles(resampledPixel[numpy.newaxis,
                                                                     numpy.newaxis,
                                                                     ...],
                                                      self.library.spectra)

                    # normalize confidence values from [pi,0] to [0,1]
                    for z in range(angles.shape[2]):
                        angles[0,0,z] = 1-angles[0,0,z]/math.pi

                    # get index of class with largest confidence value
                    indexOfMax = numpy.argmax(angles)

                    # classify pixel if confidence above threshold
                    if angles[0,0,indexOfMax] > self.threshold:

                        # index from one (after zero for no data)
                        classified[x,y] = indexOfMax + 1

        # save the classified image to a file
        spectral.io.envi.save_classification(classifiedFilename,
                                             classified,
                                             class_names=['No data']+self.library.names,
                                             metadata={
                                                 'data ignore value': 0,
                                                 'description': 'PyCOAL '+pycoal.version+' mineral classified image.',
                                                 'map info': image.metadata.get('map info')
                                             })

        # remove unused classes from the image
        pycoal.mineral.MineralClassification.filterClasses(classifiedFilename)

    @staticmethod
    def filterClasses(classifiedFilename):
        """
        Modify a classified image to remove unused classes.

        Args:
            classifiedFilename (str): file of the classified image

        Returns:
            None
        """

        # open the image
        classified = spectral.open_image(classifiedFilename)
        data = classified.asarray()
        M = classified.shape[0]
        N = classified.shape[1]

        # allocate a copy for reindexed pixels
        copy = numpy.zeros(shape=(M,N), dtype=numpy.uint16)

        # find classes actually present in the image
        classes = sorted(set(classified.asarray().flatten().tolist()))
        lookup = [classes.index(i) if i in classes else 0 for i in range(int(classified.metadata.get('classes')))]

        # reindex each pixel
        for x in range(M):
            for y in range(N):
                copy[x,y] = lookup[data[x,y,0]]

        # overwrite the file
        spectral.io.envi.save_classification(classifiedFilename,
                                             copy,
                                             force=True,
                                             class_names=[classified.metadata.get('class names')[i] for i in classes],
                                             metadata=classified.metadata)

    @staticmethod
    def toRGB(imageFilename, rgbImageFilename, red=680.0, green=532.5, blue=472.5):
        """
        Generate a three-band RGB image from an AVIRIS image and save it to a file.

        Args:
            imageFilename (str):     filename of the source image
            rgbImageFilename (str):  filename of the three-band RGB image
            red (float, optional):   wavelength in nanometers of the red band
            green (float, optional): wavelength in nanometers of the green band
            blue (float, optional):  wavelength in nanometers of the blue band

        Returns:
            None
        """

        # find the index of the first element in a list greater than the value
        def indexOfGreaterThan(elements, value):
            for index,element in enumerate(elements):
                if element > value:
                    return index

        # open the image
        image = spectral.open_image(imageFilename)

        # load the list of wavelengths as floats
        wavelengthStrings = image.metadata.get('wavelength')
        wavelengthFloats = list(map(float, wavelengthStrings))

        # find the index of the red, green, and blue bands
        redIndex = indexOfGreaterThan(wavelengthFloats, red)
        greenIndex = indexOfGreaterThan(wavelengthFloats, green)
        blueIndex = indexOfGreaterThan(wavelengthFloats, blue)

        # read the red, green, and blue bands from the image
        redBand = image[:,:,redIndex]
        greenBand = image[:,:,greenIndex]
        blueBand = image[:,:,blueIndex]

        # remove no data pixels
        for band in [redBand, greenBand, blueBand]:
            for x in range(band.shape[0]):
                for y in range(band.shape[1]):
                    if numpy.isclose(band[x,y,0], -0.005) or band[x,y,0]==-50:
                        band[x,y] = 0

        # combine the red, green, and blue bands into a three-band RGB image
        rgb = numpy.concatenate([redBand,greenBand,blueBand], axis=2)

        # update the metadata
        rgbMetadata = image.metadata
        rgbMetadata['description'] = 'PyCOAL '+pycoal.version+' three-band RGB image.'
        rgbMetadata['data ignore value'] = 0
        if wavelengthStrings:
            rgbMetadata['wavelength'] = [
                wavelengthStrings[redIndex],
                wavelengthStrings[greenIndex],
                wavelengthStrings[blueIndex]]
        if image.metadata.get('correction factors'):
            rgbMetadata['correction factors'] = [
                image.metadata.get('correction factors')[redIndex],
                image.metadata.get('correction factors')[greenIndex],
                image.metadata.get('correction factors')[blueIndex]]
        if image.metadata.get('fwhm'):
            rgbMetadata['fwhm'] = [
                image.metadata.get('fwhm')[redIndex],
                image.metadata.get('fwhm')[greenIndex],
                image.metadata.get('fwhm')[blueIndex]]
        if image.metadata.get('bbl'):
            rgbMetadata['bbl'] = [
                image.metadata.get('bbl')[redIndex],
                image.metadata.get('bbl')[greenIndex],
                image.metadata.get('bbl')[blueIndex]]
        if image.metadata.get('smoothing factors'):
            rgbMetadata['smoothing factors'] = [
                image.metadata.get('smoothing factors')[redIndex],
                image.metadata.get('smoothing factors')[greenIndex],
                image.metadata.get('smoothing factors')[blueIndex]]

        # save the three-band RGB image to a file
        spectral.envi.save_image(rgbImageFilename, rgb, metadata=rgbMetadata)

    @staticmethod
    def subsetSpectralLibrary(spectralLibrary, classNames):

        # adapted from https://git.io/v9ThM

        """
        Create a copy of the spectral library containing only the named classes.

        Args:
            spectralLibrary (SpectralLibrary): ENVI spectral library
            classNames (str[]):                list of names of classes to include

        Returns:
            SpectralLibrary: subset of ENVI spectral library
        """

        # empty array for spectra
        spectra = numpy.empty((len(classNames), len(spectralLibrary.bands.centers)))

        # empty list for names
        names = []

        # copy class spectra and names
        for newIndex, className in enumerate(classNames):
            oldIndex = spectralLibrary.names.index(className)
            spectra[newIndex] = spectralLibrary.spectra[oldIndex]
            names.append(className)

        # copy metadata
        metadata = {'wavelength units': spectralLibrary.metadata.get('wavelength units'),
                    'spectra names': names,
                    'wavelength': spectralLibrary.bands.centers }

        # return new spectral library
        return spectral.io.envi.SpectralLibrary(spectra, metadata, {})


class AsterConversion:

    def __init__(self):
        """
        This class provides a method for converting the ASTER Spectral
        Library Version 2.0 into ENVI format.

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

        asterDatabase = spectral.AsterDatabase(db_file)
        spectrumIDs = [x[0] for x in asterDatabase.query('SELECT SampleID FROM Samples').fetchall()]
        bandMin = 0.38315
        bandMax = 2.5082
        bandNum = 128
        bandInfo = spectral.BandInfo()
        bandInfo.centers = numpy.arange(bandMin, bandMax, (bandMax - bandMin) / bandNum)
        bandInfo.band_unit = 'micrometer'
        library = asterDatabase.create_envi_spectral_library(spectrumIDs, bandInfo)

        library.save(hdr_file)

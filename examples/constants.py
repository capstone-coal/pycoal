DEBUG = 1
TESTRUN = 1
PROFILE = 0

# File used if TESTRUN is set to 1.
# Contains hyperspectral data that is 0.15GB when unpacked.
# It will run relatively quickly but may have less meaningful data
# to analyze (fewer coal mines, etc.) than the large input file.
# Direct download link: ftp://avoil:Gulf0il$pill@popo.jpl.nasa.gov/y18_data/f180201t01p00r05.tar.gz
# Note that wget may not work with this FTP link due to the login credentials.
# Use your browser to download it by navigating to the link. Then move the move the file into the examples directory
# and unzip it (tar -xzf f180201t01p00r05.tar.gz)
SMALL_INPUT_NAME = "f180201t01p00r05rdn_e_sc01_ort_img"
SMALL_INPUT_FILE = "f180201t01p00r05rdn_e/" + SMALL_INPUT_NAME + ".hdr"

# File to use if TESTRUN is set to 0.
# Contains hyperspectral data that is ~18GB when unpacked
# Direct download link: ftp://avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2/ang20150420t182050_rfl_v1e/
LARGE_INPUT_NAME = "ang20150420t182050_corr_v1e_img"
LARGE_INPUT_FILE = "avng.jpl.nasa.gov/AVNG_2015_data_distribution/L2/ang20150420t182050_rfl_v1e/" + LARGE_INPUT_NAME + ".hdr"

# Use the smaller file is TESTRUN = 1, and the larger file if TESTRUN = 0
INPUT_NAME = SMALL_INPUT_NAME if TESTRUN else LARGE_INPUT_NAME
INPUT_FILENAME = SMALL_INPUT_FILE if TESTRUN else LARGE_INPUT_FILE

# Spectral library file name - change LIBRARY_FILENAME to 6 or 7 depending on which version you want to use
LIBRARY_FILENAME_6 = "s06av95a_envi.hdr"
LIBRARY_FILENAME_7 = "s07_AV95_envi.hdr"
LIBRARY_FILENAME = "../pycoal/tests/" + LIBRARY_FILENAME_7
